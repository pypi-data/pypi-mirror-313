# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""Datalayer IAM API V1."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import logging
import re
import secrets
import unicodedata
import base64

import httpx

from dataclasses import asdict
from functools import partial
from http import HTTPStatus
from urllib.parse import parse_qs, quote, unquote
from connexion import request

from datalayer_addons.credits import CheckoutPortalRequest
from datalayer_common.authn.jwt import (
    decode_jwt_token,
    extract_and_validate_external_token,
    generate_jwt_token,
    revoke_user_jwts,
)
from datalayer_common.authz import check_authz
from datalayer_common.config import JWT_EXTERNAL_ISSUER
from datalayer_solr.models import (
    HANDLE_MAX_LENGTH,
    HANDLE_MIN_LENGTH,
    HANDLE_REGEXP,
    MAIL_REGEXP,
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    PASSWORD_REGEX,
)
from datalayer_solr.models.roles import PlatformRoles
from datalayer_solr.models.usage import ResourceState, Usage
from datalayer_solr.models.user_jwt import (
    GRAVATAR_API,
    UserJWT,
)
from werkzeug.exceptions import BadRequest, Forbidden, Unauthorized

from datalayer_addons.credits import UpdateCredits

from datalayer_iam import __version__
from datalayer_iam.authz import check_proxy_url_is_allow_listed
from datalayer_iam.reserved.handles import RESERVED_HANDLES
from datalayer_iam.services.accounts import get_account_by_handle_service
from datalayer_iam.services.credits import (
    create_failed_reservation_service,
    get_account_credits_service,
    get_account_reservations_service,
    get_reservation_service,
    set_account_credits_service,
    start_reservation_service,
    stop_reservation_service,
    update_account_quota_service,
)
from datalayer_iam.services.github import (
    create_authn_github_url_service,
    github_callback_service,
)
from datalayer_iam.services.linkedin import (
    create_authn_linkedin_url_service,
    linkedin_callback_service,
)
from datalayer_iam.services.x import (
    create_authn_x_url_service,
)
from datalayer_iam.services.healthz import (
    ping_service,
)
from datalayer_iam.services.invites import (
    confirm_invite_join_event_service,
    get_invite_by_token_service,
    get_invites_sent_by_user_service,
    send_invite_service,
    send_bulk_invites_service,
    unsubscribe_invite_from_news_service,
)
from datalayer_iam.services.mails import (
    send_waitinglist_email_service,
    send_message_by_email_service,
    send_support_email_service,
)
from datalayer_iam.services.organizations import (
    add_member_role_to_organization_service,
    add_member_to_organization_service,
    create_organization_service,
    get_organization_by_handle_service,
    get_organization_member_service,
    get_organization_with_children_by_uid_service,
    get_organizations_by_type_service,
    get_organizations_for_user_service,
    remove_member_from_organization_service,
    remove_member_role_from_organization_service,
    update_organization_service,
)
from datalayer_iam.services.datasources import (
    create_datasource_service,
    get_datasource_service,
    get_datasources_service,
    update_datasource_service,
)
from datalayer_iam.services.secrets import (
    create_secret_service,
    delete_secret_service,
    get_secret_service,
    get_secrets_service,
    update_secret_service,
)
from datalayer_iam.services.teams import (
    add_member_role_to_team_service,
    add_member_to_team_service,
    create_team_service,
    get_organization_teams_service,
    get_team_by_uid_service,
    get_team_member_service,
    get_team_with_children_by_uid_service,
    remove_member_from_team_service,
    remove_member_role_from_team_service,
    update_team_service,
)
from datalayer_iam.services.tokens import (
    create_token_service,
    get_token_service,
    get_tokens_service,
    update_token_service,
)
from datalayer_iam.services.usage import (
    get_account_usage_service,
    get_platform_usage_service,
)
from datalayer_iam.services.users import (
    add_user_role_service,
    authenticate_user_service,
    confirm_user_join_with_token_service,
    create_token_for_new_password_service,
    create_url_for_new_password_service,
    create_user_join_request_service,
    create_user_join_token_request_service,
    create_user_service,
    delete_user_service,
    get_user_by_handle_service,
    get_user_by_uid_service,
    get_user_join_request_by_handle,
    get_users_by_email_service,
    has_user_role_service,
    remove_user_role_service,
    search_users_service,
    unsubscribe_user_from_news_service,
    update_profile_service,
    user_new_password_confirm_service,
)


logger = logging.getLogger(__name__)


DATALAYER_PREAMBLE_LOGO_1 = """            ___       __       __
  ───────  / _ \___ _/ /____ _/ /__ ___ _____ ____
 ───────  / // / _ `/ __/ _ `/ / _ `/ // / -_) __/
───────  /____/\_,_/\__/\_,_/_/\_,_/\_, /\__/_/
                                  /___/
"""

DATALAYER_PREAMBLE_LOGO_2 = """   ___       __       __
  / _ \___ _/ /____ _/ /__ ___ _____ ____    _________________________________________________________
 / // / _ `/ __/ _ `/ / _ `/ // / -_) __/  _________________________________________________________
/____/\_,_/\__/\_,_/_/\_,_/\_, /\__/_/   _________________________________________________________
                            /___/
"""

DATALAYER_PREAMBLE_LOGO_3 = """   ___       __       __
  / _ \___ _/ /____ _/ /__ ___ _____ ____    ________
 / // / _ `/ __/ _ `/ / _ `/ // / -_) __/  ________
/____/\_,_/\__/\_,_/_/\_,_/\_, /\__/_/   ________
                            /___/
"""

DATALAYER_PREAMBLE = f"""
<div style="padding: 10px; background-color: #282828; color: #39FF14;">
<pre>{DATALAYER_PREAMBLE_LOGO_1}
Copyright (c) Datalayer, Inc. https://datalayer.io

Accelerated and Trusted Jupyter.
</pre>
</div>
"""

REDIRECT_PREAMBLE_HTML = f"""
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">.
</head>
<body>

{DATALAYER_PREAMBLE}

<h3>Redirecting to Datalayer...</h3>

<p>Hold on tight, we are connecting with your account.</p>

</body>
"""


# FIXME This is not stateless...
__NONCE_CACHE = set()
__NONCE_USER_MAPPING_CACHE = dict()


NONCE_LINK_SEPARATOR = "__NONCE_LINK_SEPARATOR__"


# System.


def __ensure_user_is_platform_admin(user: dict):
    """TODO This is temporary and OpenFGA should be used."""
    if PlatformRoles.ADMIN.value not in user["roles"]:
        raise Forbidden()


def proxy_auth_endpoint():
    """Verifies the authentication and authorization for proxied requests.

    This endpoint is expected to be called
    - by Traefik ForwardAuth middleware.
    See: https://doc.traefik.io/traefik/middlewares/http/forwardauth/
    - or by Nginx Ingress external authentication
    See: https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#external-authentication

    It assumes the reverse proxy defines the following headers:
    Property          Forward-Request Header
    ----------------- ----------------------
    HTTP Method       X-Forwarded-Method
    Protocol          X-Forwarded-Proto
    Host              X-Forwarded-Host
    Request URI       X-Forwarded-Uri
    Source IP-Address X-Forwarded-For
    """
    authorization = request.headers.get("authorization", "")
    token = (
        authorization[7:].strip()
        if authorization.lower().startswith("bearer ")
        else None
    )
    token_dict = None if token is None else decode_jwt_token(token)

    # Bail early for OPTIONS request
    if request.headers.get("x-forwarded-method") == "OPTIONS":
        return {
            "success": True,
            "message": "Authorized",
        }

    host = request.headers.get("x-forwarded-host")
    uri = request.headers.get("x-forwarded-uri", "")
    if host and host in uri:
        _, _, uri = uri.partition(host)
    path, _, args = uri.partition("?")
    input = {
        "headers": dict(request.headers.items()),
        "host": host,
        "method": request.headers.get("x-forwarded-method"),
        "parameters": parse_qs(args, keep_blank_values=True),
        # "body": , # Needed?
        "path": path,  # str
        # "tokenHeader": , # Needed?
        "tokenPayload": token_dict,
    }

    logger.debug("Checking authorization for [%s]", input)

    # FIXME The API of check_authz has changed.
    logger.critical("The API of check_authz has changed.")
    allowed = check_authz(input)
    if allowed is False:
        logger.info(f"Forbidden request - {json.dumps(input)}")
        raise Forbidden()
    return {
        "success": True,
        "message": "Authorized",
    }


# Healthz.


async def ping_endpoint():
    """Ping."""
    resp = ping_service()
    logger.info("Pong response: [%s]", resp)
    return {
        "success": True,
        "message": "datalayer_iam is up and running.",
        "status": resp,
        "version": __version__,
    }


# Contact.


async def send_email_endpoint(body):
    """Send an email.

    FIXME This should not be so easy to send email...
    """
    account_handle = body.get("accountHandle")
    first_name = body.get("firstName")
    last_name = body.get("lastName")
    email_addresss = str(body.get("email")).lower()
    message = body.get("message")
    logger.info("Sending email to Datalayer with copy to [%s]", email_addresss)
    send_message_by_email_service(account_handle, first_name, last_name, email_addresss, message)
    return {
        "success": True,
        "message": f"Your message is sent to Datalayer with copy to {email_addresss}.",
    }, HTTPStatus.CREATED


async def register_waitinglist_endpoint(body):
    """Register to the waiting list."""
    first_name = body.get("firstName")
    last_name = body.get("lastName")
    email = str(body.get("email")).lower()
    affiliation = body.get("affiliation")
    logger.info("Sending email to [%s]", email)
    send_waitinglist_email_service(first_name, last_name, email, affiliation)
    return {
        "success": True,
        "message": f"The waiting list registration confirmation message is sent to {email}.",
    }, HTTPStatus.CREATED


def contact_endpoint(user, body):
    try:
        name = user["handle"]
        email = body.get("email") or user["email"]
        send_support_email_service(
            body["subject"], body["body"], f"{name} <{email}>"
        )
        return {"success": True, "message": "Message sent"}, HTTPStatus.CREATED
    except Exception as e:
        logger.error("Failed to send message to platform support.", e)
        return {"success": False, "message": "Message not sent"}


# Proxy.


async def proxy_request_endpoint(body):
    """Proxy request."""
    request_url = body["request_url"]
    check_proxy_url_is_allow_listed(request_url)
    request_method = body["request_method"]
    request_url = body["request_url"]
    request_token = body["request_token"]
    if request_method == "GET":
        r = httpx.get(
            request_url,
            headers = {
                "Accept": "application/json",
                "Authorization": f"Bearer {request_token}",
                "X-Restli-Protocol-Version": "2.0.0",
            },
        )
        r.raise_for_status()
        return {
            "success": True,
            "message": "Proxy GET Request executed.",
            "response": r.json(),
        }
    elif request_method == "POST":
        request_body = body["request_body"]
        r = httpx.post(
            request_url,
            headers = {
                "Accept": "application/json",
                "Authorization": f"Bearer {request_token}",
                "X-Restli-Protocol-Version": "2.0.0",
            },
            data = json.dumps(request_body),
        )
        restli = r.headers.get("X-RestLi-Id")
        r.raise_for_status()
        return {
            "success": True,
            "message": "Proxy POST Request executed.",
            "response": r.json(),
            "restli": restli,
        }
    elif request_method == "PUT":
        request_body = body["request_body"]
        content: str = request_body["content"]
        content = content.replace("data:image/png;base64,", "")
        r = httpx.put(
            request_url,
            headers = {
                "Authorization": f"Bearer {request_token}",
                "X-Restli-Protocol-Version": "2.0.0",
            },
#            content = content.encode()
            content = base64.b64decode(content)
        )
        r.raise_for_status()
        return {
            "success": True,
            "message": "Proxy PUT Request executed.",
        }
    else:
        raise Exception("Unsupported method.")


# Login / Logout.


async def login_endpoint(body):
    """Login a user with a handle/password or a token (token can be external)."""
    addon = request.state.addon

    user_handle = body.get("handle", "").lower()
    password = body.get("password")
    token = body.get("token")

    provided_token_issuer = None
    provided_token_external_issuer = None

    if token:
        # Check if the provided token is a valid external token
        # and try to deduce a user_handle.
        provided_jwt_token = extract_and_validate_external_token(token)
        if provided_jwt_token is not None:
            # The provided token is external.
            logger.debug("Extracted external JWT Token [%s] from [%s]", provided_jwt_token, token)
            provided_token_issuer = provided_jwt_token.get("iss", None)
            provided_token_external_issuer = provided_jwt_token.get("iss", JWT_EXTERNAL_ISSUER)
            logger.info("JWT external issuer [%s]", provided_token_external_issuer)
            user_handle = provided_jwt_token["sub"]
            if isinstance(user_handle, dict):
                user_handle = hashlib.sha256(json.dumps(user_handle).encode()).hexdigest()
        else:
            # Check if we are logging in with a Datalayer JWT token.
            try:
                provided_jwt_token = decode_jwt_token(token)
                provided_token_issuer = provided_jwt_token.get("iss", None)
                user_handle = provided_jwt_token["sub"]["handle"]
            except Unauthorized as e:
                # FIXME Do not log with error, we are hitting many such exceptions in production...
                logger.debug(f"Log in attempt with invalid token {token}.", exc_info=e)

        # The provided token has been validated...
        # Create a user if this is the first visit.
        if user_handle is not None:
            auth_user = None
            if user_handle != "":
                auth_user = get_user_by_handle_service(user_handle, public=False)
            if not auth_user and user_handle != "":
                # User has provided a valid token but is not yet know by Datalayer.
                # That can be the case when authenticating with an external_token.
                logger.info("Creating a new user with handle [%s] from token [%s].", user_handle, token)
                auth_user = await create_user_service(
                    user_handle=user_handle,
                    first_name="",
                    last_name="",
                    email="",
                    password="",
                    origin=provided_jwt_token.get("iss", JWT_EXTERNAL_ISSUER),
                    avatar_url="",
                    roles=None,
                    token=token,
                    addon=addon,
                )
            if auth_user is not None:
                user_jwt = UserJWT(
                    uid=auth_user["uid"],
                    handle=user_handle,
                    email=auth_user["email_s"],
                    first_name=auth_user["first_name_t"],
                    last_name=auth_user["last_name_t"],
                    avatar_url=auth_user.get("avatar_url_s"),
                    roles=auth_user["roles_ss"],
                )
                datalayer_jwt_token, _ = generate_jwt_token(user_jwt)
                return {
                    "success": True,
                    "message": "User is successfully logged in.",
                    "user": auth_user,
                    "token": datalayer_jwt_token,
                    "provided_token": token,
                    "provided_token_issuer": provided_token_issuer,
                    "is_provided_token_external": True
                    if provided_token_external_issuer is not None
                    else False,
                }, HTTPStatus.CREATED

    # Empty password should always be rejected as its the value
    # used for other authentication methods (e.g. JWT token or GitHub).
    if not user_handle or not password:
        return {
            "success": False,
            "message": "Please provide valid credentials.",
        }, HTTPStatus.UNAUTHORIZED
    logger.info("Login requested for user_handle [%s].", user_handle)
    auth_user = authenticate_user_service(user_handle, password)
    if not auth_user:
        return {
            "success": False,
            "message": "Login failed, please check your credentials.",
        }, HTTPStatus.UNAUTHORIZED
    logger.info("Login success for user_handle [%s].", user_handle)
    user_jwt = UserJWT(
        uid=auth_user["uid"],
        handle=user_handle,
        email=auth_user["email_s"],
        first_name=auth_user["first_name_t"],
        last_name=auth_user["last_name_t"],
        avatar_url=auth_user.get("avatar_url_s"),  # Is avatar_url_s not always present?
        roles=auth_user["roles_ss"],
    )
    datalayer_jwt_token, _ = generate_jwt_token(user_jwt)
    return {
        "success": True,
        "message": "User is successfully logged in.",
        "user": auth_user,
        "token": datalayer_jwt_token,
        "provided_token": token,
        "provided_token_issuer": provided_token_issuer,
        "is_provided_token_external": True if provided_token_external_issuer is not None else False,
    }, HTTPStatus.CREATED


def logout_endpoint(user):
    """Performs a logout."""
    revoke_user_jwts(user["uid"])
    return {
        "success": True,
        "message": "The authenticated user is successfully logged out."
    }


# Join.


def request_to_join_endpoint(body):
    """Request to join Datalayer."""
    warnings = []
    user_handle = str(body["handle"]).lower()
    email = str(body["email"]).lower()
    logger.info(
        "Join request for user_handle [%s] with email [%s].", user_handle, email
    )
    first_name = body["firstName"]
    last_name = body["lastName"]
    password = body["password"]
    password_confirm = body["passwordConfirm"]
    if user_handle in RESERVED_HANDLES or user_handle + "s" in RESERVED_HANDLES:
        warnings.append(f"Handle `{user_handle}` is reserved.")
    if (len(user_handle) > 0) and (
        get_user_by_handle_service(user_handle) is not None
        or get_organization_by_handle_service(user_handle) is not None
    ):
        warnings.append(f"Handle `{user_handle}` is not available.")
    if (len(get_users_by_email_service(email)) > 0):
        warnings.append(f"Email `{email}` is already registered as a user.")
    if len(user_handle) < HANDLE_MIN_LENGTH:
        warnings.append(f"Handle must be of minimal length {HANDLE_MIN_LENGTH}.")
    if len(user_handle) > HANDLE_MAX_LENGTH:
        warnings.append(f"Handle must be of maximal length {HANDLE_MAX_LENGTH}.")
#    if not user_handle.isalnum():
#        warnings.append(f"Handle `{user_handle}` contains not allowed characters.")
    if not re.match(HANDLE_REGEXP, user_handle):
        warnings.append("Handle should only contain alphanumerics or hyphens.")
    if not re.match(MAIL_REGEXP, email):
        warnings.append("Provide a valid email address.")
    error = _check_password(password, password_confirm)
    if error:
        warnings.append(error)
    if len(warnings) > 0:
        return {
            "success": False,
            "message": "Please check the information you have provided.",
            "warnings": warnings,
        }, HTTPStatus.BAD_REQUEST
    user_handle, token = create_user_join_request_service(
        user_handle, first_name, last_name, email, password
    )
    logger.info("Join request created for user [%s] with token [%s]", user_handle, token)
    return {
        "success": True,
        "message": f"We have sent an email to {email}. Please check the inbox and click on the activation link.",
    }, HTTPStatus.CREATED


async def join_user_with_invite_endpoint(body):
    """Join a user with an invite."""
    warnings = []
    token = body["token"]
    user_handle = str(body["handle"]).lower()
    email = str(body["email"]).lower()
    logger.info("Invite claimed with token [%s] for user_handle [%s] and email [%s].", token, user_handle, email)
    first_name = body["firstName"]
    last_name = body["lastName"]
    password = body["password"]
    password_confirm = body["passwordConfirm"]
    if user_handle in RESERVED_HANDLES or user_handle + "s" in RESERVED_HANDLES:
        warnings.append(f"Handle `{user_handle}` is reserved")
    if (len(user_handle) > 0) and (
        get_user_by_handle_service(user_handle) is not None
        or get_organization_by_handle_service(user_handle) is not None
    ):
        warnings.append(f"Handle `{user_handle}` is not available.")
    if len(user_handle) < HANDLE_MIN_LENGTH:
        warnings.append(f"Handle must be of minimal length {HANDLE_MIN_LENGTH}.")
    if len(user_handle) > HANDLE_MAX_LENGTH:
        warnings.append(f"Handle must be of maximal length {HANDLE_MAX_LENGTH}.")
#    if not user_handle.isalnum():
#        warnings.append(f"Handle `{user_handle}` contains not allowed characters.")
    if not re.match(HANDLE_REGEXP, user_handle):
        warnings.append("Handle should only contain alphanumerics or hyphens.")
    if not re.match(MAIL_REGEXP, email):
        warnings.append("Provide a valid email address.")

    warning = _check_password(password, password_confirm)
    if warning:
        warnings.append(warning)

    if len(warnings) > 0:
        return {
            "success": False,
            "message": "Please check the information you have provided.",
            "warnings": warnings,
        }, HTTPStatus.BAD_REQUEST
    addon = request.state.addon
    await create_user_service(
        user_handle,
        first_name,
        last_name,
        email,
        password,
        addon = addon,
    )
    confirm_invite_join_event_service(token)
    return {
        "success": True,
        "message": f"Welcome {user_handle} to Datalayer.",
    }, HTTPStatus.CREATED


def request_token_to_join_endpoint(body):
    """Request a token to join Datalayer."""
    errors = []
    user_handle = str(body["handle"]).lower()
    email = str(body["email"]).lower()
    logger.info(
        "Join request for user_handle [%s] with email [%s].", user_handle, email
    )
    first_name = body["firstName"]
    last_name = body["lastName"]
    password = body["password"]
    password_confirm = body["passwordConfirm"]
    if user_handle in RESERVED_HANDLES or user_handle + "s" in RESERVED_HANDLES:
        errors.append(f"Handle `{user_handle}` is reserved.")
    if (len(user_handle) > 0) and (
        get_user_by_handle_service(user_handle) is not None
        or get_organization_by_handle_service(user_handle) is not None
    ):
        errors.append(f"Handle `{user_handle}` is not available")
    if (len(get_users_by_email_service(email)) > 0):
        errors.append(f"Email `{email}` is already registered as a user.")
    if len(user_handle) < HANDLE_MIN_LENGTH:
        errors.append(f"Handle must be of minimal length {HANDLE_MIN_LENGTH}.")
    if len(user_handle) > HANDLE_MAX_LENGTH:
        errors.append(f"Handle must be of maximal length {HANDLE_MAX_LENGTH}.")
#    if not user_handle.isalnum():
#        warnings.append(f"Handle `{user_handle}` contains not allowed characters.")
    if not re.match(HANDLE_REGEXP, user_handle):
        errors.append("Handle should only contain alphanumerics or hyphens.")
    if not re.match(MAIL_REGEXP, email):
        errors.append("Provide a valid email address.")

    error = _check_password(password, password_confirm)
    if error:
        errors.append(error)

    if len(errors) > 0:
        return {
            "success": False,
            "message": "Please check the information you have provided.",
            "errors": errors,
        }, HTTPStatus.BAD_REQUEST
    user_handle, _ = create_user_join_token_request_service(
        user_handle, first_name, last_name, email, password
    )
    return {
        "success": True,
        "message": "We have sent you an email. Please check your inbox and fill in the activation code.",
    }, HTTPStatus.CREATED


async def join_user_with_token_endpoint(handle: str, token: str):
    """Join a user with a token."""
    handle = handle.lower()
    addon = request.state.addon
    logger.info(
        "Join confirmation request for user_handle [%s] with token [%s].",
        handle,
        token,
    )
    found_user = get_user_join_request_by_handle(handle, token, public=False)
    logger.info("Found user [%s]", found_user)
    if found_user is None:
        logger.info("Handle [%s] is not found.", handle)
        return {
            "success": False,
            # Don't give details on the error for unprotected endpoint...
            "message": "Check the user handle and confirmation token.",
        }, HTTPStatus.NOT_FOUND
    if found_user is not None and found_user.get("join_ts_dt", None) is not None:
        logger.info("Handle [%s] is not available.", handle)
        return {
            "success": False,
            # Don't give details on the error for unprotected endpoint...
            "message": "Check the user handle and confirmation token.",
        }, HTTPStatus.NOT_FOUND
    result = await confirm_user_join_with_token_service(
        handle, token, await addon.get_token_for_external_credits(request), addon
    )
    if result is not None:
        return result
    return {
        "success": True,
        "message": f"Welcome user {handle} to Datalayer.",
    }


# Password.


def _check_password(password: str, password_confirm: str) -> str | None:
    """Check a password.

    Args:
        password: Password
        password_confirm: Password confirmation
    Returns:
        The error message if the check failed
        ``None`` if the check passes
    """
    if unicodedata.normalize("NFKD", password) != unicodedata.normalize(
        "NFKD", password_confirm
    ):
        return "The passwords do not match."
    is_valid = PASSWORD_REGEX.match(password)
    if not is_valid:
        if len(password) < PASSWORD_MIN_LENGTH:
            return f"Password must be of minimal length {PASSWORD_MIN_LENGTH}."
        elif len(password) > PASSWORD_MAX_LENGTH:
            return f"Password must be of maximal length {PASSWORD_MAX_LENGTH}."
        else:
            return "Password must contain at least one lower case letter, one upper case letter, one digit and one special character."


def request_url_for_new_password_endpoint(body):
    """Request a new password."""
    errors = []
    user_handle = body["handle"].lower()
    password = body["password"]
    password_confirm = body["passwordConfirm"]
    error = _check_password(password, password_confirm)
    if error:
        errors.append(error)
    if len(errors) > 0:
        return {
            "success": False,
            "message": "Please correct the information you have provided.",
            "errors": errors,
        }, HTTPStatus.BAD_REQUEST
    resp = create_url_for_new_password_service(user_handle, password)
    logger.info("Forgot password response [%s]", resp)
    return resp, HTTPStatus.OK


def request_token_for_new_password_endpoint(body):
    """Request a token for a new password"""
    errors = []
    user_handle = body["handle"].lower()
    password = body["password"]
    password_confirm = body["passwordConfirm"]
    error = _check_password(password, password_confirm)
    if error:
        errors.append(error)
    if len(errors) > 0:
        return {
            "success": False,
            "message": "Please correct the information you have provided.",
            "errors": errors,
        }, HTTPStatus.BAD_REQUEST
    resp = create_token_for_new_password_service(user_handle, password)
    logger.info("Forgot password response [%s]", resp)
    return resp, HTTPStatus.CREATED


def confirm_new_password_endpoint(handle, token):
    """Confirm a new password request."""
    logger.info(
        "New Password confirmation requested for user_handle [%s] and token [%s].",
        handle,
        token,
    )
    response = user_new_password_confirm_service(handle, token)
    logger.info("New password confirmation result [%s].", response)
    return response, HTTPStatus.OK


# Profile.


def get_me_endpoint(user):
    """Get me."""
    logger.info("Current authenticated user [%s]", user)
    return {
        "success": True,
        "message": "Current authenticated user.",
        "me": user,
    }


def get_authn_user_endpoint(user):
    """Get the authenticated user account."""
    user_handle = user["handle"]
    profile = get_user_by_handle_service(user_handle, public=False)
    if not profile.get("avatar_url_s"):
        # Update user profile with gravatar.
        hashed_email = hashlib.md5(profile["email_s"].lower().encode()).hexdigest()
        avatar_url = f"{GRAVATAR_API}/{hashed_email}"
        profile["avatar_url_s"] = avatar_url
        try:
            update_profile_service(user_handle, {"avatar_url_s": {"set": avatar_url}})
        except Exception as e:
            logger.warn("Failed to set user avatar URL.", exc_info=e)
    logger.info(
        "Found authenticated user with user_handle [%s] [%s]",
        user_handle,
        profile,
    )
    return {
        "success": True,
        "message": "The authenticated user details are retrieved.",
        "profile": profile,
    }


def update_authn_profile_endpoint(user, body):
    """Update the account of the authenticated user."""
    user_handle = user["handle"]
    first_name = body["firstName"]
    last_name = body["lastName"]
    email = body.get("email")
    result = update_profile_service(user_handle, first_name, last_name, email)
    return result


# Accounts.


def delete_authn_account_endpoint(user):
    """Remove the account of the authenticated user."""
    user_handle = user["handle"]
    profile = get_user_by_handle_service(user_handle)
    logger.info("Remove the account of user_handle [%s] [%s]", user_handle, profile)
    delete_user_service(user_handle)
    return None, HTTPStatus.NO_CONTENT


def get_account_by_handle_endpoint(handle):
    """Get the account."""
    user = None
    organization = None
    account = get_account_by_handle_service(handle, public=False)
    if account is not None:
        if account.type_s == "user":
            user = asdict(account)
        if account.type_s == "organization":
            organization = asdict(account)
    return {
        "success": True,
        "message": "The account (user or organization) is retrieved.",
        "user": user,
        "organization": organization,
    }


# News.


def unsubscribe_user_news_endpoint(id):
    """Unsubscribe a user from news."""
    result = unsubscribe_user_from_news_service(id)
    if result is not None:
        return {
            "success": True,
            "message": "The user is unsubscribed and will not receive further news from Datalayer.",
        }
    else:
        return {
            "success": False,
            "message": "We can not find the user.",
        }, HTTPStatus.BAD_REQUEST


def unsubscribe_from_news_by_token_endpoint(token):
    """Unsubscribe invite from news."""
    result = unsubscribe_invite_from_news_service(token)
    if result is not None:
        return {"success": True, "message": "You are unsubscribed."}
    else:
        return {
            "success": False,
            "message": "We can not find you.",
        }, HTTPStatus.BAD_REQUEST


# Users.


def get_user_by_uid_endpoint(id, user):
    """Get a user details."""
    if user['uid'] != id:
        __ensure_user_is_platform_admin(user) # TODO This is temporary and OpenFGA should be used.
    user_by_uid = get_user_by_uid_service(id)
    return {
        "success": True,
        "message": "The user is retrieved.",
        "user": user_by_uid,
    }


def search_users_endpoint(user, body):
    """Search users."""
    naming_pattern = body.get("namingPattern")
    logger.info("Searching users with pattern [%s]", naming_pattern)
    as_platform_admin = PlatformRoles.ADMIN.value in user["roles"]
    users = search_users_service(naming_pattern, as_platform_admin=as_platform_admin)
    return {
        "success": True,
        "message": "The users have been searched.",
        "users": users,
    }


def check_user_role_endpoint(id: str, role: str):
    """Check if a user has a given role."""
    return {
        "success": True,
        "message": "The user role is checked.",
        "check": has_user_role_service(id, role),
    }


async def add_user_role_endpoint(user, id: str, role: str):
    """Add a role to a user."""
    add_user_role_service(id, role)
    # Revoke the token as the user role needs to be updated.
    revoke_user_jwts(id)
    return {"success": True, "message": "Role is added to the user."}


async def remove_user_role_endpoint(user, id: str, role: str):
    """Remove a role from a user."""
    remove_user_role_service(id, role)
    # Revoke the token as the user role needs to be updated.
    revoke_user_jwts(id)
    return {"success": True, "message": "Role is removed from the user."}


# Invites.


def get_invite_by_token_endpoint(token):
    """Get an invite by token."""
    logger.info("Getting invite with token [%s]", token)
    invite = get_invite_by_token_service(token)
    logger.info("Found invite [%s] for token [%s]", invite, token)
    return {
        "success": True,
        "invite": invite,
    }


def get_invites_sent_by_user_endpoint(id):
    """Get the invites sent by a user."""
    invites = get_invites_sent_by_user_service(id)
    return {
        "success": True,
        "message": "The invites have been retrieved.",
        "invites": invites,
    }


def send_invite_endpoint(user, body):
    """Send an invite to join the platform."""
    warnings = []
    email = str(body["email"]).lower()
    first_name = body["firstName"]
    last_name = body["lastName"]
    message = body["message"]
    if not re.match(MAIL_REGEXP, email):
        warnings.append("Provide a valid email address.")
    if (len(get_users_by_email_service(email)) > 0):
        warnings.append(f"Email `{email}` is already registered as a user.")
    if len(warnings) > 0:
        return {
            "success": False,
            "message": "Check the information you have provided.",
            "warnings": warnings,
        }, HTTPStatus.BAD_REQUEST
    logger.info("Creating invite from [%s] to [%s]", user, email)
    from_user = UserJWT.from_subject(user)
    invite = send_invite_service(from_user, first_name, last_name, email, message)
    return {
        "success": True,
        "message": f"We have sent an invite to {email}.",
        "invite": invite,
    }, HTTPStatus.CREATED


def send_bulk_invites_endpoint(user, body):
    """Send bulk invites to join the platform."""
    from_user = UserJWT.from_subject(user)
    invitees = send_bulk_invites_service(from_user, body)
    return {
        "success": True,
        "message": f"We are sending the invites.",
        "invitees": invitees,
    }, HTTPStatus.CREATED


# Credits.


async def get_credits_endpoint(user: dict):
    """Get authenticated user credits balance."""
    try:
        addon = request.state.addon
        credits = await get_account_credits_service(
            user["uid"],
            await addon.get_token_for_external_credits(request),
            addon,
        )
        return {
            "success": True,
            "credits": {
                "credits": credits.credits,
                "quota": credits.limit,
                "last_update": credits.last_update,
            },
            "reservations": list(
                map(
                    lambda r: {
                        "id": r.resource_uid,
                        "credits": r.credits_limit,
                        "resource": r.resource_uid,
                        "last_update": r.updated_at,
                        "burning_rate": r.burning_rate,
                        "start_date": r.start_date,
                    },
                    get_account_reservations_service(user["uid"]),
                )
            ),
        }
    except (ValueError, RuntimeError) as e:
        logger.error("Unable to get credits for user %s", user["handle"], exc_info=e)
        return {"success": False, "message": str(e)}


async def get_user_credits_endpoint(user: dict, id: str):
    """Get credits for a user."""
    try:
        addon = request.state.addon
        credits = await get_account_credits_service(
            id,
            await addon.get_token_for_external_credits(request),
            addon,
        )
        logger.info("User user_uid [%s] has now credits [%s]", id, credits)
        return {
            "success": True,
            "message": f"User {id} has {credits.credits} credits.",
            "credits": {
                "credits": credits.credits,
                "quota": credits.limit,
                "last_update": credits.last_update,
            },
        }
    except (ValueError, RuntimeError) as e:
        logger.error("Unable to get credits for user %s", user["handle"], exc_info=e)
        return {"success": False, "message": str(e)}


async def update_user_credits_endpoint(user: dict, id: str, body: dict):
    """Update (add/remove) credits for (to/from) a user."""
    try:
        credits_update = UpdateCredits(
            account_uid=id,
            credits=body["credits"],
        )
        logger.info("Updating user_uid [%s] credits with [%s]", id, credits_update)
        credits = await set_account_credits_service(credits_update)
        logger.info("User user_uid [%s] has now credits [%s]", id, credits)
        return {
            "success": True,
            "message": f"User {id} has been successfully updated and has now {credits.credits} credits.",
            "credits": {
                "credits": credits.credits,
                "quota": credits.limit,
                "last_update": credits.last_update,
            },
        }
    except (ValueError, RuntimeError) as e:
        logger.error("Unable to get credits for user %s", user["handle"], exc_info=e)
        return {"success": False, "message": str(e)}


async def get_quota_endpoint(user: dict, user_uid: str | None = None):
    """Get user quota."""
    addon = request.state.addon
    try:
        credits = await get_account_credits_service(
            user_uid or user["uid"],
            await addon.get_token_for_external_credits(request),
            addon,
        )
        return {
            "success": True,
            "credits": {
                "credits": credits.credits,
                "quota": credits.limit,
                "last_update": credits.last_update,
            },
        }
    except (ValueError, RuntimeError) as e:
        logger.error("Unable to get quota for user %s", user_uid, exc_info=e)
        return {"success": False, "message": str(e)}


async def update_quota_endpoint(user: dict, body: dict):
    """Update a user quota."""
    addon = request.state.addon
    try:
        credits = await update_account_quota_service(
            body.get("user_uid", user["uid"]),
            body["quota"],
            body.get("reset", "1") == "1",
            "update_quota_endpoint",
            token=await addon.get_token_for_external_credits(request),
            addon=addon,
        )
        return {
            "success": True,
            "credits": {
                "credits": credits.credits,
                "quota": credits.limit,
                "last_update": credits.last_update,
            },
        }
    except (ValueError, RuntimeError) as e:
        logger.error(
            "Unable to update quota for user %s", body["user_handle"], exc_info=e
        )
        return {"success": False, "message": str(e)}, HTTPStatus.BAD_REQUEST


def _format_reservation(usage: Usage, include_account: bool = False) -> dict:
    serialized = {
        "id": usage.resource_uid,
        "credits": usage.credits_limit,
        "resource": usage.resource_uid,
        "resource_type": usage.resource_type,
        "last_update": usage.updated_at,
        "burning_rate": usage.burning_rate,
        "start_date": usage.start_date,
    }

    if include_account:
        serialized["account_uid"] = usage.account_uid

    return serialized


def _filter_reservation_type(resource_type: str | None, usage: Usage) -> bool:
    return resource_type is None or resource_type in usage.resource_type.split(";")


def get_reservations_endpoint(user: dict, type: str | None = None) -> dict:
    """Get user reservations."""
    has_user = request.headers.get("x-api-key") is None
    return {
        "success": True,
        "reservations": list(
            map(
                lambda r: _format_reservation(r, not has_user),
                filter(
                    partial(_filter_reservation_type, type),
                    get_account_reservations_service(
                        user["uid"] if has_user else None, type
                    ),
                ),
            )
        ),
    }


def get_reservation_endpoint(user: dict, id: str):
    """Get a reservation."""
    reservation = get_reservation_service(user["uid"], id)
    if reservation is not None:
        return {
            "success": True,
            "reservation": {
                "id": reservation.resource_uid,
                "credits": reservation.credits_limit,
                "resource": reservation.resource_uid,
                "last_update": reservation.updated_at,
                "burning_rate": reservation.burning_rate,
                "start_date": reservation.start_date,
            },
        }
    else:
        return {
            "success": False,
            "message": "No reservation found",
        }, HTTPStatus.NOT_FOUND


async def create_reservation_endpoint(body):
    """Internal REST endpoint to create a resource reservation."""
    addon = request.state.addon
    account_uid = request.headers.get("x-forwarded-user")
    if account_uid is None:
        return {
            "success": False,
            "message": "Missing account UID",
        }, HTTPStatus.BAD_REQUEST
    if "resource_uid" in body:
        usage = await start_reservation_service(
            account_uid=account_uid,
            burning_rate=body["burning_rate"],
            pod_resources=body.get("pod_resources"),
            reservation=body["reservation"],
            resource_given_name=body.get("resource_given_name"),
            resource_type=body["resource_type"],
            resource_uid=body["resource_uid"],
            resource_state=ResourceState(
                body.get("resource_state", ResourceState.RUNNING.value)
            ),
            token=await addon.get_token_for_external_credits(request),
            addon=addon,
        )
    else:
        usage = await create_failed_reservation_service(
            account_uid=account_uid,
            reservation=body["reservation"],
            resource_type=body["resource_type"],
            resource_state=ResourceState(body["resource_state"]),
        )
    return {
        "success": True,
        "message": "Reservation created.",
        "reservation": {
            "id": usage.resource_uid,
            **{
                k: v
                for k, v in dataclasses.asdict(usage).items()
                if k != "checkout_uid"
            },
        },
    }, HTTPStatus.CREATED


async def delete_reservation_endpoint(id: str, event: str = "deleted"):
    """Internal REST endpoint to terminate a reservation for a pod."""
    addon = request.state.addon
    account_uid = request.headers.get("x-forwarded-user")
    if account_uid is None:
        return {
            "success": False,
            "message": "Missing account UID",
        }, HTTPStatus.BAD_REQUEST
    await stop_reservation_service(
        account_uid=account_uid,
        reservation_uid=id,
        event=event,
        token=await addon.get_token_for_external_credits(request),
        addon=addon,
    )
    return None, HTTPStatus.NO_CONTENT


async def create_checkout_portal_endpoint(user, body):
    """Get the checkout portal information."""
    addon = request.state.addon
    portal = await addon.get_checkout_portal(
        user["uid"],
        CheckoutPortalRequest(**body),
        await addon.get_token_for_external_credits(request),
    )
    if portal is None:
        return {
            "success": True,
        }
    # If the target URL is relative, assume it is relative to the IAM server.
    if portal.url is not None and portal.url.startswith("/"):
        portal = dataclasses.replace(
            portal, url=f"{request.url.scheme}://{request.url.netloc}" + portal.url
        )
    return {
        "success": True,
        "portal": dataclasses.asdict(portal),
    }


# Organizations.


def create_organization_endpoint(user, body):
    """Create an organization."""
    warnings = []
    organization_handle = str(body["handle"]).lower()
    if (
        organization_handle in RESERVED_HANDLES
        or organization_handle + "s" in RESERVED_HANDLES
    ):
        warnings.append(f"Handle `{organization_handle}` is reserved.")
    if (len(organization_handle) > 0) and (
        get_user_by_handle_service(organization_handle) is not None
        or get_organization_by_handle_service(organization_handle) is not None
    ):
        warnings.append(f"Handle `{organization_handle}` is not available.")
    if len(organization_handle) < HANDLE_MIN_LENGTH:
        warnings.append(f"Handle must be of minimal length {HANDLE_MIN_LENGTH}.")
    if len(organization_handle) > HANDLE_MAX_LENGTH:
        warnings.append(f"Handle must be of maximal length {HANDLE_MAX_LENGTH}.")
    if not re.match(HANDLE_REGEXP, organization_handle):
        warnings.append("Handle should only contain alphanumerics or hyphens.")
    if len(warnings) > 0:
        return {
            "success": False,
            "message": "Check the information you have provided",
            "warnings": warnings,
        }, HTTPStatus.BAD_REQUEST
    organization = create_organization_service(user, body)
    return {
        "success": True,
        "message": "The organization is created.",
        "organization": organization,
    }, HTTPStatus.CREATED


def update_organization_endpoint(id, body):
    """Update an organization."""
    update_organization_service(id, body)
    return {
        "success": True,
        "message": "The organization is updated.",
    }


def get_organization_endpoint(id):
    """Get an organization by handle."""
    organization = get_organization_with_children_by_uid_service(id)
    return {
        "success": True,
        "message": "The organization is retrieved.",
        "organization": organization,
    }


def get_organizations_by_type_endpoint(type):
    """Get organizations by type."""
    organizations = get_organizations_by_type_service(type, True)
    return {
        "success": True,
        "message": "The organizations are retrieved.",
        "organizations": organizations,
    }


def get_organizations_endpoint(user):
    """Get the organizations for the authenticated user."""
    organizations = get_organizations_for_user_service(user["handle"])
    return {
        "success": True,
        "message": "The organizations are retrieved.",
        "organizations": organizations,
    }


def add_member_to_organization_endpoint(id, user_id):
    """Add a user as member to an organization."""
    user = get_user_by_uid_service(user_id)
    add_member_to_organization_service(id, user)
    return {
        "success": True,
        "message": "The user is added as member to the organization.",
    }


def remove_member_from_organization_endpoint(id, user_id):
    """Remove a member from an organization."""
    member = get_organization_member_service(id, user_id, public=False)
    remove_member_from_organization_service(member)
    return {
        "success": True,
        "message": "The member is removed from the organization.",
    }


def add_member_role_to_organization_endpoint(id, user_id, role):
    """Add a member role to an organization."""
    member = get_organization_member_service(id, user_id, public=False)
    logger.info("Retrieved organization member [%s]", member)
    add_member_role_to_organization_service(member, role)
    return {
        "success": True,
        "message": "The user role is added to the member of the organization.",
    }


def remove_member_role_from_organization_endpoint(id, user_id, role):
    """Remove a role from an organization member."""
    member = get_organization_member_service(id, user_id, public=False)
    logger.info("Retrieved organization member [%s]", member)
    remove_member_role_from_organization_service(member, role)
    return {
        "success": True,
        "message": "The role is removed from the organization member.",
    }


# Teams.


def create_team_endpoint(user, body):
    """Create a team."""
    warnings = []
    team_handle = str(body["handle"]).lower()
    organization_uid = body["organizationId"]
    if team_handle in RESERVED_HANDLES or team_handle + "s" in RESERVED_HANDLES:
        warnings.append(f"Handle `{team_handle}` is reserved.")
    if (len(team_handle) > 0) and (
        get_team_by_uid_service(organization_uid, team_handle) is not None
    ):
        warnings.append(f"Handle `{team_handle}` is not available.")
    if len(team_handle) < HANDLE_MIN_LENGTH:
        warnings.append(f"Handle must be of minimal length {HANDLE_MIN_LENGTH}.")
    if len(team_handle) > HANDLE_MAX_LENGTH:
        warnings.append(f"Handle must be of maximal length {HANDLE_MAX_LENGTH}.")
    if not re.match(HANDLE_REGEXP, team_handle):
        warnings.append("Handle should only contain alphanumerics or hyphens.")
    if len(warnings) > 0:
        return {
            "success": False,
            "message": "Check the information you have provided",
            "warnings": warnings,
        }, HTTPStatus.BAD_REQUEST
    team = create_team_service(user, body)
    return {
        "success": True,
        "message": "The team is created.",
        "team": team,
    }, HTTPStatus.CREATED


def get_organization_teams_endpoint(id):
    """Get organization teams."""
    teams = get_organization_teams_service(id)
    logger.info("Retrieved [%s] teams for organization_uid [%s]", len(teams), id)
    return {
        "success": True,
        "message": "The teams are retrieved.",
        "teams": teams,
    }


def get_team_endpoint(id):
    """Get a team by id."""
    team = get_team_with_children_by_uid_service(id)
    return {
        "success": True,
        "message": "The team is retrieved.",
        "team": team,
    }


def update_team_endpoint(id, body):
    """Update a team."""
    update_team_service(id, body)
    return {
        "success": True,
        "message": "The team is updated.",
    }


def add_member_to_team_endpoint(id, user_id):
    """Add a user as member to a team."""
    user = get_user_by_uid_service(user_id)
    add_member_to_team_service(id, user)
    return {
        "success": True,
        "message": "The user is added as member to the team.",
    }


def remove_member_from_team_endpoint(id, user_id):
    """Remove a member from a team."""
    member = get_team_member_service(id, user_id, public=False)
    remove_member_from_team_service(member)
    return {
        "success": True,
        "message": "The member is removed from the team.",
    }


def add_member_role_to_team_endpoint(id, user_id, role):
    """Add a member role to a team."""
    member = get_team_member_service(id, user_id, public=False)
    logger.info("Retrieved team member [%s]", member)
    add_member_role_to_team_service(member, role)
    return {
        "success": True,
        "message": "The user role is added to the member of the team.",
    }


def remove_member_role_from_team_endpoint(id, user_id, role):
    """Remove a role from a team member."""
    member = get_team_member_service(id, user_id, public=False)
    logger.info("Retrieved team member [%s]", member)
    remove_member_role_from_team_service(member, role)
    return {
        "success": True,
        "message": "The role is removed from the team member.",
    }


# Data Sources.


def create_datasource_endpoint(user, body):
    """Create a datasource."""
    datasource = create_datasource_service(user, body)
    return {
        "success": True,
        "message": "The datasource is created.",
        "datasource": datasource,
    }, HTTPStatus.CREATED


def get_datasources_endpoint(user):
    """Get the datasources."""
    datasources = get_datasources_service(user)
    logger.info("Retrieved [%s] datasources", len(datasources))
    return {
        "success": True,
        "message": "The datasources are retrieved.",
        "datasources": datasources,
    }


def get_datasource_endpoint(user, id):
    """Get a datasource by handle."""
    datasource = get_datasource_service(user, id)
    return {
        "success": True,
        "message": "The datasource is retrieved.",
        "datasource": datasource,
    }


def update_datasource_endpoint(user, id, body):
    """Update a datasource."""
    update_datasource_service(user, id, body)
    return {
        "success": True,
        "message": "The datasource is updated.",
    }


# Secrets.


def create_secret_endpoint(user, body):
    """Create a secret."""
    secret = create_secret_service(user, body)
    return {
        "success": True,
        "message": "The secret is created.",
        "secret": secret,
    }, HTTPStatus.CREATED


def get_secrets_endpoint(user):
    """Get the secrets."""
    secrets = get_secrets_service(user)
    logger.info("Retrieved [%s] secrets", len(secrets))
    return {
        "success": True,
        "message": "The secrets are retrieved.",
        "secrets": secrets,
    }


def get_secret_endpoint(user, id):
    """Get a secret by handle."""
    secret = get_secret_service(user, id)
    return {
        "success": True,
        "message": "The secret is retrieved.",
        "secret": secret,
    }


def update_secret_endpoint(user, id, body):
    """Update a secret."""
    update_secret_service(user, id, body)
    return {
        "success": True,
        "message": "The secret is updated.",
    }


def delete_secret_endpoint(user, id):
    """Delete a secret."""
    delete_secret_service(user, id)
    return {
        "success": True,
        "message": "The secret is deleted.",
    }


# Tokens.


def create_token_endpoint(user, body):
    """Create a token."""
    token = create_token_service(user, body)
    return {
        "success": True,
        "message": "The token is created.",
        "token": token,
    }, HTTPStatus.CREATED


def get_tokens_endpoint(user):
    """Get the tokens."""
    tokens = get_tokens_service(user)
    logger.info("Retrieved [%s] tokens", len(tokens))
    return {
        "success": True,
        "message": "The tokens are retrieved.",
        "tokens": tokens,
    }


def get_token_endpoint(user, id):
    """Get a token by handle."""
    token = get_token_service(user, id)
    return {
        "success": True,
        "message": "The token is retrieved.",
        "token": token,
    }


def update_token_endpoint(user, id, body):
    """Update a token."""
    update_token_service(user, id, body)
    return {
        "success": True,
        "message": "The token is updated.",
    }


# Usage


def get_user_usage_endpoint(user):
    usages = get_account_usage_service(user["uid"])
    return {
        "success": True,
        "message": f"Usage for {user['uid']}",
        "usages": list(
            map(
                lambda usage: {
                    k: v
                    for k, v in dataclasses.asdict(usage).items()
                    if k != "checkout_uid"
                },
                usages,
            )
        ),
    }


def get_platform_usage_endpoint():
    usages = get_platform_usage_service()
    return {
        "success": True,
        "message": f"Usage for the platform",
        "usages": list(
            map(
                lambda usage: {
                    k: v
                    for k, v in dataclasses.asdict(usage).items()
                    if k != "checkout_uid"
                },
                usages,
            )
        ),
    }


# OAuth2.


def oauth2_authz_url_link_endpoint(user, provider: str, callback_uri: str):
    """Create the appropriate OAuth2 authorization URL for the given provider to link with the Datalayer account."""
    user_nonce = secrets.token_urlsafe(8)
    __NONCE_USER_MAPPING_CACHE[user_nonce] = user["uid"]
    return oauth2_authz_url_endpoint(provider, callback_uri, None, user_nonce)


def oauth2_authz_url_endpoint(provider: str, callback_uri: str, nonce: str = "", user_nonce = None):
    """Create the appropriate OAuth2 authorization URL for the given provider.

    Args:
        provider: OAuth2 provider
        callback_uri: URI to be called with the authenticated user profile and token
        nonce: Nonce to be validated by the callback URI
    """
    # TODO How secure is it to rely on a provided nonce?
#    nonce = nonce or secrets.token_urlsafe(16)
    nonce = secrets.token_urlsafe(16)
    if user_nonce is not None:
        nonce = NONCE_LINK_SEPARATOR + user_nonce + NONCE_LINK_SEPARATOR + nonce
    __NONCE_CACHE.add(nonce)
    headers = request.headers
    forwarded_host = headers.get(
        "x-forwarded-host", headers.get("X-Forwarded-Host", "")
    )
    forwarded_protocol = headers.get(
        "x-forwarded-proto", headers.get("X-Forwarded-Proto", "")
    )
    base_url = (
        f"{forwarded_protocol}://{forwarded_host}"
        if forwarded_host
        else f"{request.url.scheme}://{request.url.netloc}"
    )
    splitted = re.split(r"(?<=v\d)\/", request.url.path, maxsplit=1)
    if len(splitted) == 1:
        splitted = re.split(r"(?<=v\d\d)\/", request.url.path, maxsplit=1)
    if base_url.endswith("/"):
        base_url = base_url[:-1]
    base_url += splitted[0]
    if provider == "github":
        authorization_url = create_authn_github_url_service(
            base_url, f"{nonce}:{quote(callback_uri, safe='')}"
        )
    elif provider == "linkedin":
        authorization_url = create_authn_linkedin_url_service(
            base_url, f"{nonce}:{quote(callback_uri, safe='')}"
        )
    elif provider == "x":
        authorization_url = create_authn_x_url_service(
            base_url, f"{nonce}:{quote(callback_uri, safe='')}"
        )
    else:
        raise BadRequest(f"{provider} is not a supported provider.")
    return {
        "success": True,
        "message": f"Authorization URL for {provider} iam provider.",
        "autorization_url": authorization_url,
    }


async def oauth2_github_callback_endpoint(
    state: str,
    code: str = "",
    error: str = "",
    error_description: str = "",
    error_uri: str = "",
):
    """OAuth2 callback for GitHub.

    Args:
        code: OAuth2 code to request token
        state: OAuth2 state payload
    """
    nonce, _, callback_uri = state.partition(":")
    if nonce not in __NONCE_CACHE:
        raise Unauthorized("Invalid state.")
    else:
        __NONCE_CACHE.remove(nonce)
    if error:
        error_ = f"{error} {error_description}".strip()
        return f"""<h3>Redirecting to Datalayer...</h3>
            <p>Failed to authenticate with GitHub.</p>
            <script>
                window.location.replace('{unquote(callback_uri)}?_xsrf={nonce}&provider=github&error={error_}')
            </script>
            """
    user_uid = None
    if nonce.startswith(NONCE_LINK_SEPARATOR):
        result = re.search(NONCE_LINK_SEPARATOR + '(.*)' + NONCE_LINK_SEPARATOR, nonce)
        user_nonce = result.group(1)
        user_uid = __NONCE_USER_MAPPING_CACHE[user_nonce]
    user_profile, token, github_access_token = await github_callback_service(code, user_uid, request.state.addon)
    user = quote(json.dumps(user_profile), safe="")
    return f"""{REDIRECT_PREAMBLE_HTML}
        <script>
            window.location.replace('{unquote(callback_uri)}?_xsrf={nonce}&token={token}&user={user}&github_access_token={github_access_token}')
        </script>
        """


async def oauth2_linkedin_callback_endpoint(
    state: str,
    code: str = "",
    error: str = "",
    error_description: str = "",
    error_uri: str = "",
):
    """OAuth2 callback for LinkedIn.

    Attached to the redirect_uri are two important URL arguments that you need to read from the request:

    code — The OAuth 2.0 authorization code.
    state — A value used to test for possible CSRF attacks.

    The code is a value that you exchange with LinkedIn for an OAuth 2.0 access token in the next step of the authentication process.
    For security reasons, the authorization code has a 30-minute lifespan and must be used immediately.
    If it expires, you must repeat all of the previous steps to request another authorization code.

    Args:
        code: OAuth2 code to request token
        state: OAuth2 state payload
    """
    nonce, _, callback_uri = state.partition(":")
    if nonce not in __NONCE_CACHE:
        raise Unauthorized("Invalid state.")
    else:
        __NONCE_CACHE.remove(nonce)
    if error:
        error_ = f"{error} {error_description}".strip()
        return f"""<h3>Redirecting to Datalayer...</h3>
            <p>Failed to authenticate with LinkedIn.</p>
            <script>
                window.location.replace('{unquote(callback_uri)}?_xsrf={nonce}&provider=linkedin&error={error_}')
            </script>
            """
    headers = request.headers
    forwarded_host = headers.get(
        "x-forwarded-host", headers.get("X-Forwarded-Host", "")
    )
    forwarded_protocol = headers.get(
        "x-forwarded-proto", headers.get("X-Forwarded-Proto", "")
    )
    # FIXME We had to prefix with api/iam/v1
    base_url = (
        f"{forwarded_protocol}://{forwarded_host}"
        if forwarded_host
        else f"{request.url.scheme}://{request.url.netloc}"
    ) + "/api/iam/v1"
    user_uid = None
    if nonce.startswith(NONCE_LINK_SEPARATOR):
        result = re.search(NONCE_LINK_SEPARATOR + '(.*)' + NONCE_LINK_SEPARATOR, nonce)
        user_nonce = result.group(1)
        user_uid = __NONCE_USER_MAPPING_CACHE[user_nonce]
    user_profile, token, linkedin_access_token = await linkedin_callback_service(code, base_url, user_uid, request.state.addon)
    user = quote(json.dumps(user_profile), safe="")
    return f"""{REDIRECT_PREAMBLE_HTML}
        <script>
            window.location.replace('{unquote(callback_uri)}?_xsrf={nonce}&token={token}&user={user}&linkedin_access_token={linkedin_access_token}')
        </script>
        """


# FIXME
# @app.route("/api/iam/school", methods=["POST"])
# def create_school_endpoint(body):
#     """Create a school."""
#     user = get_user_jwt()
#     school = create_school_service(user, body)
#     return jsonify(
#         {
#             "success": True,
#             "school": school,
#             "message": "The school is created.",
#         }
#     )


# FIXME
# @app.route("/api/iam/school", methods=["PUT"])
# def update_school_endpoint(body):
#     """Update a school."""
#     update_school_service(body)
#     return jsonify(
#         {
#             "success": True,
#             "message": "The school is updated.",
#         }
#     )
