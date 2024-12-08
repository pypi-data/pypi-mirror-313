# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""LinkedIn service."""

import logging
from urllib.parse import quote, urlencode

import httpx
from werkzeug.exceptions import NotFound, Unauthorized

from datalayer_iam.config import (
    DATALAYER_LINKEDIN_CLIENT_ID,
    DATALAYER_LINKEDIN_CLIENT_SECRET,
)
from datalayer_iam.model import (
    DatalayerUrn,
)
from datalayer_addons.credits import ABCCreditsAddon
from datalayer_iam.services.users import (
    create_user_service,
    get_user_for_linked_iam_provider_service,
    link_user_to_iam_provider_service,
)
from datalayer_solr.models.user_jwt import (
    UserJWT,
)
from datalayer_common.authn.jwt import generate_jwt_token
from datalayer_solr.accounts import (
    get_user_by_handle,
    get_user_by_origin,
    get_user_by_uid,
)


LINKEDIN_LOGIN_AUTHZ_URL = "https://linkedin.com/oauth/v2/authorization"

LINKEDIN_LOGIN_ACCESS_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"

LINKEDIN_USER_INFO_URL = "https://api.linkedin.com/v2/userinfo"


logger = logging.getLogger(__name__)


def __fetch_access_token(code: str, base_url: str, ) -> dict:
    """
    grant_type	string	The value of this field should always be: authorization_code - Yes
    code	string	The authorization code you received in Step 2 - Yes
    client_id	string	The Client ID value generated in Step 1 - Yes
    client_secret	string	The Secret Key value generated in Step 1. See the Best Practices Guide for ways to keep your client_secret value secure - Yes
    redirect_uri	url	The same redirect_uri value that you passed in the previous step.

    Docs:
        https://learn.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow?tabs=HTTPS1#step-3-exchange-authorization-code-for-an-access-token
    """
    if base_url.endswith("/"):
        base_url = base_url[:-1]
    data = {
        "grant_type": "authorization_code",
        "client_id": DATALAYER_LINKEDIN_CLIENT_ID,
        "client_secret": DATALAYER_LINKEDIN_CLIENT_SECRET,
        "code": code,
        "redirect_uri": "/".join((base_url, "oauth2/linkedin/callback")),
    }
    r = httpx.post(
        LINKEDIN_LOGIN_ACCESS_TOKEN_URL,
        data=data,
        headers={"Accept": "application/json"},
    )
    r.raise_for_status()
    return r.json()


def __fetch_user_info(access_token: str) -> dict:
    """ Get LinkedIn user info form LinkedIn API

    Docs:
        https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access
        https://learn.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow

    Response Example:
        {
            'sub': 'DUfL...',
            'email_verified': True,
            'name': 'Eric Charles',
            'locale': {'country': 'US', 'language': 'en'},
            'given_name': 'Eric',
            'family_name': 'Charles',
            'email': 'eric@datalayer.io',
            'picture': 'https://media.licdn.com/dms/image/v2/D4E03AQGY5Cz5X3TGvA/profile-displayphoto-shr'
        }
    """
    r = httpx.get(
        LINKEDIN_USER_INFO_URL,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    r.raise_for_status()
    return r.json()


def create_authn_linkedin_url_service(base_url: str, state: str) -> str:
    """Build the LinkedIn login request URL.

    Args
        base_url: IAM service base URL
        state: OAuth state value
    Returns
        The LinkedIn.com login OAuth URL
    """
    if not DATALAYER_LINKEDIN_CLIENT_ID or not DATALAYER_LINKEDIN_CLIENT_SECRET:
        raise NotFound("No LinkedIn client available.")
    if base_url.endswith("/"):
        base_url = base_url[:-1]
    qs = urlencode(
        {
            "client_id": DATALAYER_LINKEDIN_CLIENT_ID,
            "redirect_uri": "/".join((base_url, "oauth2/linkedin/callback")),
            "response_type": "code",
            "state": state,
            "scope": "openid profile w_member_social email",
        },
        quote_via=quote,
    )
    return f"{LINKEDIN_LOGIN_AUTHZ_URL}?{qs}"


async def linkedin_callback_service(code: str, base_url: str, link_user_uid: str | None, addon: ABCCreditsAddon) -> tuple[dict, str]:
    """LinkedIn App OAuth callback.

    Args:
        code: Authentication flow code
        callback_uri: URI to call with the authenticated token
    Returns:
        The user private profile and the authentication token
    """
    token_data = __fetch_access_token(code, base_url)
    if "access_token" in token_data:
        linkedin_access_token = token_data["access_token"]
        linkedin_user_info = __fetch_user_info(linkedin_access_token)
        linkedin_account_id = linkedin_user_info["sub"]
        first_name = linkedin_user_info["given_name"]
        last_name = linkedin_user_info["family_name"]
        handle = linkedin_user_info["sub"]
        email = linkedin_user_info.get("email")
        urn = DatalayerUrn("iam", "ext", "", "linkedin", linkedin_account_id)
        origin = urn.to_string()
        # Try to find an existing user (1) already linked (2) authenticated via linkedin.
        if link_user_uid is not None:
            user = get_user_by_uid(link_user_uid, public=False)
            if not user:
                raise Unauthorized("No user found.")
        else:
            user = get_user_for_linked_iam_provider_service("linkedin", linkedin_account_id)
        if not user:
            user = get_user_by_origin(origin, public=False)
        # If no existing user has been found, create it and link it.
        if not user:
            logger.info("No existing user found for origin [%s] and linkedin_account_id [%s] - Creating a new user.", origin, linkedin_account_id)
            handle = origin
            # Check the handle is not yet used...
            user_ = get_user_by_handle(handle)
            if user_:
                raise Unauthorized(
                    f"A user with handle {handle} already exists. Unable to log in with LinkedIn."
                )
            # Create user avatar.
            avatar_url = linkedin_user_info.get("picture")
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
            link_user_to_iam_provider_service(user["uid"], "linkedin", linkedin_account_id)
        else:
            logger.info("Found existing user for email [%s] and linkedin_account_id [%s]: [%s].", email, linkedin_account_id, user)
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
        return user, jwt_token, linkedin_access_token
    else:
        raise Unauthorized(
            "LinkedIn App authorized but unable to get a token for the code."
        )
