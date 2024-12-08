# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""GitHub service.

This is inspired by:
- https://docs.github.com/en/apps/creating-github-apps/writing-code-for-a-github-app/building-a-login-with-github-button-with-a-github-app
- for the security (CSRF and redirect): https://github.com/oauth2-proxy/oauth2-proxy/blob/e3dc927e570700ae598425344cf07073965bd19c/oauthproxy.go
"""

import logging
from urllib.parse import quote, urlencode

import httpx
from werkzeug.exceptions import NotFound, Unauthorized

from datalayer_iam.config import (
    DATALAYER_GITHUB_CLIENT_ID,
    DATALAYER_GITHUB_CLIENT_SECRET,
)
from datalayer_addons.credits import ABCCreditsAddon
from datalayer_iam.services.users import (
    create_user_service,
    get_user_for_linked_iam_provider_service,
    link_user_to_iam_provider_service,
)
from datalayer_iam.model import (
    DatalayerUrn,
)
from datalayer_solr.models.user_jwt import (
    GRAVATAR_API,
    UserJWT,
)
from datalayer_common.authn.jwt import generate_jwt_token
from datalayer_solr.accounts import (
    get_user_by_handle,
    get_user_by_origin,
    get_user_by_uid,
)


GITHUB_LOGIN_AUTHZ_URL = "https://github.com/login/oauth/authorize"

GITHUB_LOGIN_ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"

GITHUB_USER_INFO_URL = "https://api.github.com/user"


logger = logging.getLogger(__name__)


def __fetch_access_token(code: str) -> dict:
    r = httpx.post(
        GITHUB_LOGIN_ACCESS_TOKEN_URL,
        data={
            "client_id": DATALAYER_GITHUB_CLIENT_ID,
            "client_secret": DATALAYER_GITHUB_CLIENT_SECRET,
            "code": code,
        },
        headers={
            "Accept": "application/json"
        },
    )
    r.raise_for_status()
    return r.json()


def __fetch_user_info(access_token: str) -> dict:
    """ Get GitHub user info form GitHub API

    Read https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#get-the-authenticated-user
    """
    r = httpx.get(
        GITHUB_USER_INFO_URL,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {access_token}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    r.raise_for_status()
    return r.json()


def create_authn_github_url_service(base_url: str, state: str) -> str:
    """Build the GitHub login request URL.

    Args
        base_url: IAM service base URL
        state: OAuth state value
    Returns
        The GitHub.com login OAuth URL
    """
    if not DATALAYER_GITHUB_CLIENT_ID or not DATALAYER_GITHUB_CLIENT_SECRET:
        raise NotFound("No GitHub client available.")
    if base_url.endswith("/"):
        base_url = base_url[:-1]
    qs = urlencode(
        {
            "client_id": DATALAYER_GITHUB_CLIENT_ID,
            "redirect_uri": "/".join((base_url, "oauth2/github/callback")),
            "response_type": "code",
            "state": state,
        },
        quote_via=quote,
    )
    return f"{GITHUB_LOGIN_AUTHZ_URL}?{qs}"


async def github_callback_service(code: str, link_user_uid: str | None, addon: ABCCreditsAddon) -> tuple[dict, str]:
    """GitHub App OAuth callback.

    Args:
        code: Authentication flow code
    Returns:
        The user private profile and the authentication token
    """
    token_data = __fetch_access_token(code)
    if "access_token" in token_data:
        github_access_token = token_data["access_token"]
        github_user_info = __fetch_user_info(github_access_token)
        github_account_id = github_user_info["id"]
        first_name, _, last_name = github_user_info["name"].partition(" ")
        email = github_user_info.get("email")
        if not email:
            # FIXME TBC GitHub user profile may not return an email.
            logger.error("No public email in the returned GitHub account.")
            raise Exception("Check you GitHub profile has a public email address...")
        urn = DatalayerUrn("iam", "ext", "", "github", github_account_id)
        origin = urn.to_string()
        # Try to find an existing user (1) already linked (2) authenticated via github.
        if link_user_uid is not None:
            user = get_user_by_uid(link_user_uid, public=False)
            if not user:
                raise Unauthorized("No user found.")
        else:
            user = get_user_for_linked_iam_provider_service("github", github_account_id)
        if not user:
            user = get_user_by_origin(origin, public=False)
        # If no existing user has been found, create it and link it.
        if not user:
            logger.info("No existing user found for origin [%s] and github_account_id [%s] - Creating a new user.", origin, github_account_id)
            handle = origin
            # Check the handle is not yet used...
            user_ = get_user_by_handle(handle)
            if user_:
                raise Unauthorized(f"A user with handle {handle} already exists. Unable to log in with GitHub.")
            # Create user avatar.
            if github_user_info.get("gravatar_id"):
                avatar_url = f"{GRAVATAR_API}/{github_user_info['gravatar_id']}"
            else:
                avatar_url = github_user_info["avatar_url"]
            # Create the user.
            user = await create_user_service(
                handle,
                first_name,
                last_name,
                email,
                "",
                origin,
                avatar_url,
                addon=addon,
            )
            # Link the user.
            link_user_to_iam_provider_service(user["uid"], "github", github_account_id)
        else:
            logger.info("Found existing user for email [%s] and github_account_id [%s]: [%s].", email, github_account_id, user)
        user_jwt = UserJWT(
            uid = user["uid"],
            handle = user["handle_s"],
            email = user["email_s"],
            first_name = user["first_name_t"],
            last_name = user["last_name_t"],
            avatar_url = user.get("avatar_url_s"),
            roles = user["roles_ss"],
        )
        jwt_token, _ = generate_jwt_token(user_jwt)
        return user, jwt_token, github_access_token
    else:
        raise Unauthorized(
            "GitHub App authorized but unable to get a token for the code."
        )
