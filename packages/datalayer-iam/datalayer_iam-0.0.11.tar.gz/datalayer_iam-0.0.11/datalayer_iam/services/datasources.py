# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""Datalayer Data Sources service."""

import logging

from datalayer_solr.utils import new_ulid
from datalayer_solr.datasources import (
    create_datasource,
    get_datasources,
    get_datasource,
    update_datasource,
)


logger = logging.getLogger(__name__)


def create_datasource_service(user, body):
    """Create a datasource."""
    datasource = {
        "uid": new_ulid(),
        "user_uid": user["uid"],
        "type_s": "datasource",
        "name_s": body["name"],
        "description_t": body["description"],
        "variant_s": body["variant"],
        "database_s": body["database"],
        "output_bucket_s": body["outputBucket"],
    }
    create_datasource(datasource)
    return datasource


def get_datasources_service(user):
    return get_datasources(user["uid"])


def get_datasource_service(user, uid):
    """Get a datasource by uid."""
    return get_datasource(user["uid"], uid)


def update_datasource_service(user, uid, body):
    """Update a datasource by uid."""
    datasource = get_datasource_service(user, uid)
    datasource["name_s"] = {"set": body["name"]}
    datasource["description_t"] = {"set": body["description"]}
    datasource["database_s"] = {"set": body["database"]}
    datasource["output_bucket_s"] = {"set": body["output_bucket"]}
    update_datasource(datasource)
