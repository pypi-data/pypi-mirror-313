# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""Datalayer Users service."""

import hashlib
import logging
from functools import partial

from http import HTTPStatus
from urllib.parse import urlparse

# from datalayer_common.authz import put_authz
from datalayer_addons.credits import UpdateCredits

from datalayer_addons.credits import ABCCreditsAddon

from datalayer_common.utils import (
    create_tmp_token_password,
    extract_password_from_token,
    hash_password,
    verify_password,
)
from datalayer_common.config import DATALAYER_CDN_URL
from datalayer_iam.config import INITIAL_USER_CREDITS
from datalayer_iam.services.credits import (
    create_account_credits_service,
    set_account_credits_service,
)
from datalayer_iam.services.mails import (
    send_support_email_service,
    send_email_service,
)

from datalayer_solr.models.roles import (
    PlatformRoles,
    SpaceRoles,
)
from datalayer_solr.accounts import (
    confirm_user_password_with_token,
    create_user,
    delete_user,
    get_account_by_uid,
    get_user_for_linked_iam_provider,
    get_user_by_handle,
    get_user_by_uid,
    get_users_by_email,
    get_user_join_request_by_handle,
    search_users,
    link_user_to_iam_provider,
    update_user,
    verify_user_handle_password,
)
from datalayer_solr.spaces import (
    SPACE_DEFAULT_VARIANT,
    create_space,
)
from datalayer_solr.utils import (
    now_string,
    new_ulid,
    new_uuid,
    sanitize_query_value,
)
from datalayer_solr.models.user_jwt import GRAVATAR_API
from datalayer_solr.defaults.cell import INIT_MATPLOTLIB_CELL
from datalayer_solr.defaults.output import OUTPUTSHOT_PLACEHOLDER_URL


logger = logging.getLogger("__name__")


def create_user_join_request_service(
    user_handle, first_name, last_name, email, password
):
    """Create a temporary user and notify the user by email."""
    token = new_ulid()
    user = {
        "id": new_uuid(),
        "uid": new_ulid(),
        "type_s": "user_join_request",
        "handle_s": user_handle,
        "email_s": email,
        "first_name_t": first_name,
        "last_name_t": last_name,
        "join_request_ts_dt": now_string(),
        "password_tmp_s": create_tmp_token_password(token, password),
        "roles_ss": [
            PlatformRoles.GUEST.value,
        ],
    }
    create_user(user)
    """
    put_authz(
        [
            {
                "op": "add",
                "target": "entity",
                "value": {
                    "uid": {"type": "User", "id": user["uid"]},
                    "attrs": {"handle": user["handle_s"]},
                    "parents": [{"type": "UserRole", "id": Roles.GUEST.value}],
                },
            }
        ]
    )
    """
    # You may find the following resources helpful as you familiarize yourself with Datalayer.
    # User Guide: https://github.com/datalayer/datalayer
    # Issue Tracker: https://github.com/datalayer/datalayer/issues
    text = f"""Thanks for signing up for Datalayer!

Please click the link below to confirm activation of your Datalayer account:

{DATALAYER_CDN_URL}/join/confirm/user/{user_handle}/{token}

Datalayer is currently an early-release service. We appreciate your
feedback, questions and suggestions. As appropriate, we encourage you 
to email our support group.

Email Support: support@datalayer.io

Happy Data Analysis!

Sincerely, The Datalayer Team.
"""
    logger.info("👏 Sending invite mail to [%s] with content:\n%s", email, text)
    send_email_service(email, "Ξ 👏 A warm welcome from Datalayer", text)
    return user_handle, token


def create_user_join_token_request_service(
    user_handle, first_name, last_name, email, password
):
    """Create a temporary user and notify the user by email."""
    token = new_ulid()
    user = {
        "id": new_uuid(),
        "uid": new_ulid(),
        "type_s": "user_join_request",
        "handle_s": user_handle,
        "email_s": email,
        "first_name_t": first_name,
        "last_name_t": last_name,
        "join_request_ts_dt": now_string(),
        "password_tmp_s": create_tmp_token_password(token, password),
        "roles_ss": [
            PlatformRoles.GUEST.value,
        ],
    }
    create_user(user)
    """
    put_authz(
        [
            {
                "op": "add",
                "target": "entity",
                "value": {
                    "uid": {"type": "User", "id": user["uid"]},
                    "attrs": {"handle": user["handle_s"]},
                    "parents": [{"type": "UserRole", "id": Roles.GUEST.value}],
                },
            }
        ]
    )
    """
    # You may find the following resources helpful as you familiarize yourself with Datalayer.
    # User Guide: https://github.com/datalayer/datalayer
    # Issue Tracker: https://github.com/datalayer/datalayer/issues
    text = f"""Thanks for signing up for Datalayer!

Please use the activation code below to confirm your Datalayer account:

{token}

Datalayer is currently an early-release service. We appreciate your
feedback, questions and suggestions. As appropriate, we encourage you 
to email our support group.

Email Support: support@datalayer.io

Happy Data Analysis!

Sincerely, The Datalayer Team.
"""
    logger.info("👏 Sending invite mail to [%s] with content:\n%s", email, text)
    send_email_service(email, "Ξ 👏 A warm welcome from Datalayer", text)
    return user_handle, token


async def confirm_user_join_with_token_service(
    user_handle, token, addon_token: str | None = None, addon: str | None = None
):
    """Confirm user join."""
    error, user = confirm_user_password_with_token(
        user_handle, token, extract_password_from_token, new=True
    )
    if error is not None:
        logger.info(error)
        return {
            "success": False,
            # Don't give details on the error for unprotected endpoint.
            "message": "Check the user handle and confirmation token.",
        }, HTTPStatus.NOT_FOUND
    """
    put_authz(
        [
            {
                "op": "add",
                "uid": {"type": "User", "id": user["uid"]},
                "target": "parent",
                "value": {"type": "UserRole", "id": Roles.MEMBER.value},
            },
            {
                "op": "remove",
                "uid": {"type": "User", "id": user["uid"]},
                "target": "parent",
                "value": {"type": "UserRole", "id": Roles.GUEST.value},
            },
        ]
    )
    """
    await bootstrap_user_service(user, addon_token, addon)
    logger.info("User [%s] is confirmed.", user_handle)


async def create_user_service(
    user_handle,
    first_name,
    last_name,
    email,
    password,
    origin="datalayer",
    avatar_url="",
    roles=None,
    token: str | None = None,
    addon: ABCCreditsAddon | None = None,
) -> dict:
    """Create a user.

    Args:
        origin: Identity provider
    """
    roles_ = []
    if roles is not None:
        for role in roles:
            try:
                PlatformRoles(role)
            except ValueError:
                logger.warning(f"Role {role} is unknown - skipping it.")
            else:
                roles_.append(role)
    if not roles_:
        roles_.append(PlatformRoles.MEMBER.value)
    if not avatar_url:
        hashed_email = hashlib.md5(email.lower().encode()).hexdigest()
        avatar_url = f"{GRAVATAR_API}/{hashed_email}"
#    else:
#        # Drop query args and fragment (it is set in the frontend) - !!! this is breaking e.g. the LinkedIn avatar.
#        o = urlparse(avatar_url)
#        avatar_url = o._replace(fragment="", query="", params="").geturl()
    user = {
        "id": new_uuid(),
        "uid": new_ulid(),
        "type_s": "user",
        "handle_s": user_handle,
        "email_s": email,
        "first_name_t": first_name,
        "last_name_t": last_name,
        "join_ts_dt": now_string(),
        "origin_s": origin,
        "password_s": hash_password(password),
        "avatar_url_s": avatar_url,
        "roles_ss": roles_,
    }
    create_user(user)
    """
    put_authz(
        [
            {
                "op": "add",
                "target": "entity",
                "value": {
                    "uid": {"type": "User", "id": user["uid"]},
                    "attrs": {"handle": user["handle_s"]},
                    "parents": [{"type": "UserRole", "id": role} for role in roles_],
                },
            }
        ]
    )
    """
    await bootstrap_user_service(user, token, addon)
    if PlatformRoles.GUEST.value in roles_:
        send_support_email_service(
            "A new guest registered",
            f"""The new user guest {user_handle} <{email}> registered from {origin}.

You need to add him/her the role 'user'. So he/she can access the Datalayer cloud features.
""",
        )

    logger.info("👏 User [%s] is created and bootstrapped", user_handle)
    return user


def delete_user_service(user_handle: str):
    """Remove a user."""
    user = delete_user(user_handle)
    """
    put_authz(
        [
            {
                "op": "remove",
                "uid": {"type": "User", "id": user["uid"]},
                "target": "entity",
            }
        ]
    )
    """
    logger.info("User [%s] deleted", user_handle)


async def bootstrap_user_service(
    user: dict, token: str | None = None, addon: ABCCreditsAddon | None = None
):
    """Bootstrap a user.

    - Create its credits account (depending on the available addon).
    - Create a default space (called "library") populated with a cell and an exercise.
    """
    user_handle = user["handle_s"]
    user_uid = user["uid"]
    logger.info("Bootstraping user [%s]", user_handle)
    try:
        bootstrap_credits = addon.bootstrap_credits if addon is not None else INITIAL_USER_CREDITS
        await create_account_credits_service(user, token, addon)        
        credits_update = UpdateCredits(
            account_uid=user_uid,
            credits=bootstrap_credits,
        )
        logger.info("Bootstraping user_uid [%s] with [%s] credits with [%s]", user_uid, bootstrap_credits, credits_update)
        await set_account_credits_service(credits_update)
    except (ValueError, RuntimeError) as e:
        logger.error(
            "Failed to initiate a credits account for user [%s]",
            user_handle,
            exc_info=e,
        )

    email = user["email_s"]
    first_name = user["first_name_t"]
    last_name = user["last_name_t"]
    cell = {
        "id": new_uuid(),
        "uid": new_ulid(),
        "type_s": "cell",
        "name_t": "Cell example",
        "description_t": "A cell example",
        "source_t": INIT_MATPLOTLIB_CELL,
        "output_cdn_url_s": OUTPUTSHOT_PLACEHOLDER_URL,
        "handle_s": user_handle,
        "email_s": email,
        "first_name_t": first_name,
        "last_name_t": last_name,
        "public_b": False,
    }
    exercise = {
        "id": new_uuid(),
        "uid": new_ulid(),
        "type_s": "exercise",
        "name_t": "Exercise example",
        "description_t": "An exercise example",
        "help_t": """Use the assignment operator "=" to create the variable "x".""",
        "code_pre_t": "# Insert your preliminary code here.",
        "code_solution_t": """# Create a variable x, equals to 3.
x = 3

# Print x.
print(x)""",
        "code_question_t": """# Create a variable x, equals to 3.
...

# Print x.
...""",
        "code_test_t": """Ex().check_object("x")
Ex().check_object("x").has_equal_value()
Ex().has_output("3")
print('Congratulations. You have succeeded this exercise.')""",
        "handle_s": user_handle,
        "email_s": email,
        "first_name_t": first_name,
        "last_name_t": last_name,
        "public_b": False,
    }
    space = {
        "id": new_uuid(),
        "uid": new_ulid(),
        "handle_s": "library",
        "type_s": "space",
        "variant_s": SPACE_DEFAULT_VARIANT,
        "name_t": "Library space",
        "description_t": f"The library space for user {user['handle_s']}.",
        "user_uid": user_uid,
        "tags_ss": [
            "library",
        ],
        "members": [
            {
                "id": new_uuid(),
                "type_s": "space_member",
                "uid": user_uid,
                "handle_s": user_handle,
                "email_s": email,
                "first_name_t": first_name,
                "last_name_t": last_name,
                "roles_ss": [
                    SpaceRoles.MEMBER.value,
                ],
            }
        ],
        "items": [
            cell,
            exercise,
        ],
    }
    # TODO use create_space_service method instead...
    create_space(space)
    # TODO Create the school if first-time TLD...
    # create_school_service_for_user(user)


def create_url_for_new_password_service(user_handle, password):
    """User new password."""
    user = get_user_by_handle(user_handle, public=False)
    if not user:
        return {
            "success": False,
            "message": f"Handle [{user_handle}] does not exist.",
        }
    logger.debug("Found user [%s]", user)
    email = user.get("email_s", None)
    if not email:
        return {
            "success": False,
            "message": "No email found for user [{user_handle}].",
        }
    logger.info("Found user with email [%s]", email)
    token = new_ulid()
    password_tmp = create_tmp_token_password(token, password)
    update_user(
        user_handle,
        {
            "id": user["id"],
            "new_password_request_ts_dt": now_string(),
            "password_tmp_s": {"set": password_tmp},
        },
        deep_update=False,
    )

    text = f"""Thanks for using Datalayer!

Someone has requested to change the password of your Datalayer account.

If you have not created this request, just FORGET this mail.

Please click the link below if you have made this request:

{DATALAYER_CDN_URL}/password/confirm/user/{user_handle}/{token}

Datalayer is currently an early-release service.  We appreciate your
feedback, questions and suggestions. As appropriate, we encourage you 
to email our support group.

Email Support: support@datalayer.io

Happy Data Analysis!

Sincerely, The Datalayer Team.
"""
    logger.info("Sending mail to [%s] with content [%s]", email, text)
    send_email_service(email, "Ξ 🛂 Password Reset Request for Datalayer", text)

    return {
        "success": True,
        "message": "Check your mail and click on the activation link to reset your password.",
    }


def create_token_for_new_password_service(user_handle, password):
    """Create a token for new password."""
    user = get_user_by_handle(user_handle, public=False)
    if not user:
        return {
            "success": False,
            "message": f"Handle [{user_handle}] does not exist.",
        }
    logger.debug("Found user [%s]", user)
    email = user.get("email_s", None)
    if not email:
        return {
            "success": False,
            "message": "No email found for user [{user_handle}].",
        }
    logger.info("Found user with email [%s]", email)
    token = new_ulid()
    password_tmp = create_tmp_token_password(token, password)
    update_user(
        user_handle,
        {
            "id": user["id"],
            "new_password_request_ts_dt": now_string(),
            "password_tmp_s": {"set": password_tmp},
        },
        deep_update=False,
    )
    text = f"""Thanks for using Datalayer!

Someone has requested to change the password of your Datalayer account.

If you have not created this request, just FORGET this mail.

Please use the activation code below if you have made this request:

{token}

Datalayer is currently an early-release service.  We appreciate your
feedback, questions and suggestions. As appropriate, we encourage you 
to email our support group.

Email Support: support@datalayer.io

Happy Data Analysis!

Sincerely, The Datalayer Team.
"""
    logger.info("Sending mail to [%s] with content [%s]", email, text)
    send_email_service(email, "Ξ 🛂 Password Reset Request for Datalayer", text)
    return {
        "success": True,
        "message": "Check your mail and click on the activation link to reset your password.",
    }


def user_new_password_confirm_service(user_handle, token):
    """User new password confirm."""
    result = confirm_user_password_with_token(
        user_handle, token, extract_password_from_token
    )
    if isinstance(result, str):
        logger.error("Error while confirming the new password", result)
        return {
            "success": False,
            # Don't give details on the error for unprotected endpoint.
            "message": "Check the user handle and confirmation token.",
        }, HTTPStatus.NOT_FOUND

    logger.info(
        "Password change is successfully confirmed for user_handle [%s].", user_handle
    )
    return {
        "success": True,
        "message": f"Welcome back {user_handle}.",
    }


def authenticate_user_service(user_handle, password):
    """Authenticate a user with a handle and a password."""
    user = get_user_by_handle(user_handle, public=False)
    if not user:
        return None
    if verify_user_handle_password(user_handle, partial(verify_password, password)):
        return user
    return None


def get_user_by_handle_service(user_handle, public=True):
    """Get a user by handle."""
    return get_user_by_handle(user_handle, public)


def get_users_by_email_service(user_email, public=False):
    """Get users by email."""
    return get_users_by_email(user_email, public)


def get_user_by_uid_service(user_uid, public=True):
    """Get a user by uid."""
    return get_user_by_uid(user_uid, public)


def get_user_join_request_by_handle_sevice(user_handle, token, public=True):
    """Get a user joint request by handle."""
    return get_user_join_request_by_handle(user_handle, token, public)


def search_users_service(naming_pattern, as_platform_admin=False):
    """Search users with a naming pattern."""
    naming_pattern = sanitize_query_value(naming_pattern)
    search_query = f"first_name_t:{naming_pattern}* OR last_name_t:{naming_pattern}* OR handle_s:{naming_pattern}*"
    return search_users(search_query, as_platform_admin, sanitize=False)


def update_profile_service(
    user_handle,
    first_name: dict | str,
    last_name: str | None = None,
    email: str | None = None,
):
    """Update the user profile.

    The email can only be set if the known user does not have a known email
    and if its login method is not password - otherwise attacker may change
    the email and reset the user password.

    Args:
        user_handle: User unique handle
        first_name: New user first name
        last_name: [optional] New user last name
        email: [optional] New user email
    """
    logger.info("Updating profile for %s", user_handle)
    user = get_user_by_handle(user_handle, public=False)
    if not user:
        return {
            "success": False,
            "message": f"No user profile found for user handle [{user_handle}]",
        }
    updates = {
        "id": user["id"],
    }
    if isinstance(first_name, str):
        updates["first_name_t"] = {"set": first_name}
    else:
        updates.update(first_name)
    if last_name is not None:
        updates["last_name_t"] = {"set": last_name}
    """
    TODO Review this for security reasons.
    if email is not None:
        if not user["email_s"] and user["origin_s"] not in {
            "cli",
            "datalayer",
            "github",
        }:
            logger.warning(f"Updating email for user '{user_handle}' to {email}")
            updates["email_s"] = {"set": email}
        else:
            logger.warning(f"Skip updating email for user '{user_handle}'.")
    """
    update_user(
        user_handle,
        updates,
        deep_update=True,
    )
    return {
        "success": True,
        "message": "The user details are updated.",
    }


def unsubscribe_user_from_news_service(user_uid):
    """Unsubscribe a user from news service."""
    user = get_account_by_uid(user_uid)
    if user is not None:
        update_user(
            user["handle_s"],
            {
                "id": user["id"],
                "unsubscribe_from_news_b": {"set": True},
            },
        )
    return user


def add_user_role_service(user_uid: str, role: str) -> dict:
    """Add a role to the user

    Args:
        handle: User UID
        role: User role
    Returns:
        User description
    """
    user = get_user_by_uid(user_uid, public=False)
    if user is not None:
        roles = user.get("roles_ss", [])
        if role not in roles:
            logger.info("Adding role [%s] to user %s", role, user["handle_s"])
            update_user(
                user["handle_s"],
                {
                    "id": user["id"],
                    "roles_ss": {"add": role},
                },
            )
            """
            put_authz(
                [
                    {
                        "op": "add",
                        "uid": {"type": "User", "id": user["uid"]},
                        "target": "parent",
                        "value": {"type": "UserRole", "id": role},
                    }
                ]
            )
            """
            roles.append(role)
        user["roles_ss"] = roles
    return user


def add_user_role_by_handle_service(user_handle: str, role: str) -> dict:
    """Add a role to the user

    Args:
        user_handle: User Handle
        role: User role
    Returns:
        User description
    """
    user = get_user_by_handle(user_handle, public=False)
    if user is not None:
        roles = user.get("roles_ss", [])
        if role not in roles:
            logger.info("Adding role [%s] to user %s", role, user["handle_s"])
            update_user(
                user["handle_s"],
                {
                    "id": user["id"],
                    "roles_ss": {"add": role},
                },
            )
            roles.append(role)
        user["roles_ss"] = roles
    return user


def remove_user_role_service(user_uid: str, role: str) -> dict:
    """Remove a role from a user

    Args:
        user_uid: User UID
        role: User role
    Returns:
        User description
    """
    user = get_user_by_uid(user_uid, public=False)
    if user is not None:
        roles = user.get("roles_ss", [])
        if role in roles:
            logger.info("Removing role [%s] for user %s", role, user["handle_s"])
            update_user(
                user["handle_s"],
                {
                    "id": user["id"],
                    "roles_ss": {"remove": role},
                },
            )
            """
            put_authz(
                [
                    {
                        "op": "remove",
                        "uid": {"type": "User", "id": user["uid"]},
                        "target": "parent",
                        "value": {"type": "UserRole", "id": role},
                    }
                ]
            )
            """
            roles.remove(role)
        user["roles_ss"] = roles
    return user


def remove_user_role_by_handle_service(user_handle: str, role: str) -> dict:
    """Remove a role from a user

    Args:
        user_handle: User Handle
        role: User role
    Returns:
        User description
    """
    user = get_user_by_handle(user_handle, public=False)
    if user is not None:
        roles = user.get("roles_ss", [])
        if role in roles:
            logger.info("Removing role [%s] for user %s", role, user["handle_s"])
            update_user(
                user["handle_s"],
                {
                    "id": user["id"],
                    "roles_ss": {"remove": role},
                },
            )
            roles.remove(role)
        user["roles_ss"] = roles
    return user


def has_user_role_service(user_uid: str, role: str) -> bool:
    """Whether a user has the given role or not.

    Args:
        handle: User UID
        role: User role
    Returns:
        Result
    """
    user = get_user_by_uid(user_uid, public=False)
    if user is not None:
        roles = user.get("roles_ss", [])
        return role in roles
    return False


def link_user_to_iam_provider_service(user_uid: str, iam_provider_name: str, iam_provider_account_id: str) -> None:
    """Link a iam provider with a user."""
    link_user_to_iam_provider(user_uid, iam_provider_name, str(iam_provider_account_id))


def get_user_for_linked_iam_provider_service(iam_provider_name: str, iam_provider_account_id: str, public: bool = True) -> None:
    """Get user for linked iam provider."""
    get_user_for_linked_iam_provider(iam_provider_name, str(iam_provider_account_id), public)
