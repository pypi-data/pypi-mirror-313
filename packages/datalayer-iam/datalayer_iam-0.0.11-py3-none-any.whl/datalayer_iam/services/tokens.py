# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""Datalayer Tokens service."""

import logging

from datetime import datetime

from datalayer_solr.utils import to_iso_string
from datalayer_solr.models.roles import (
    PlatformRoles,
)
from datalayer_solr.tokens import (
    create_token,
    get_tokens,
    get_token,
    update_token,
)
from datalayer_solr.models.user_jwt import (
    UserJWT,
)
from datalayer_common.authn.jwt import (
    generate_jwt_token,
)


logger = logging.getLogger("__name__")


def create_token_service(user, body):
    """Create a token."""
    expiration_ts = datetime.fromtimestamp(body["expirationDate"] / 1e3)
    user_jwt = UserJWT(
        uid=user["uid"],
        handle=user["handle"],
        email=user.get("sub", {}).get("mail", ""),
        first_name=user.get("sub", {}).get("firstName", ""),
        last_name=user.get("sub", {}).get("lastName", ""),
        avatar_url="",
        roles=[
            PlatformRoles.MEMBER.value,
            PlatformRoles.USER_TOKEN.value,
        ]
    )
    logger.info("Creating token with expiration date [%s]", expiration_ts)
    jwt_token, uid = generate_jwt_token(user_jwt, datetime.timestamp(expiration_ts))
    token = {
        "uid": uid,
        "user_uid": user["uid"],
        "type_s": "token",
        "name_s": body["name"],
        "description_t": body["description"],
        "variant_s": body["variant"],
        "value_s": jwt_token,
        "expiration_ts_dt": to_iso_string(expiration_ts),
    }
    create_token(token)
    token["value_s"] = jwt_token
    return token


def get_tokens_service(user):
    return get_tokens(user["uid"])


def get_token_service(user, uid, with_value = False):
    """Get a token by uid by user."""
    return get_token(user["uid"], uid, with_value)

"""
def get_token_by_value_service(user, token_value):
    return get_token_by_value(user["uid"], token_value)
"""

def update_token_service(user, uid, body):
    """Update a token by uid."""
    token = get_token_service(user, uid)
    token["name_s"] = {"set": body["name"]}
    token["description_t"] = {"set": body["description"]}
    update_token(token)
