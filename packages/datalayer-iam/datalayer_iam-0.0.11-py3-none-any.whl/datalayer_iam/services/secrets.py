# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""Datalayer Secrets service."""

import logging

from datalayer_solr.utils import new_ulid
from datalayer_solr.secrets import (
    create_secret,
    delete_secret,
    get_secrets,
    get_secret,
    update_secret,
)


logger = logging.getLogger("__name__")


def create_secret_service(user, body):
    """Create a secret."""
    secret = {
        "uid": new_ulid(),
        "user_uid": user["uid"],
        "type_s": "secret",
        "name_s": body["name"],
        "description_t": body["description"],
        "variant_s": body["variant"],
        "value_s": body["value"],
    }
    create_secret(secret)
    return secret


def get_secrets_service(user):
    return get_secrets(user["uid"])


def get_secret_service(user, uid):
    """Get a secret by uid."""
    return get_secret(user["uid"], uid)


def update_secret_service(user, uid, body):
    """Update a secret by uid."""
    secret = get_secret_service(user, uid)
    secret["name_s"] = {"set": body["name"]}
    secret["description_t"] = {"set": body["description"]}
    secret["value_s"] = {"set": body["value"]}
    update_secret(secret)


def delete_secret_service(user, uid):
    """Delete a secret by uid."""
    delete_secret(user["uid"], uid)
