# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""Datalayer Usage service."""

from datalayer_solr.usage import (
    get_account_usage,
    get_platform_usage,
)


def get_account_usage_service(user_uid):
    """Get account usage service."""
    return get_account_usage(user_uid)


def get_platform_usage_service():
    """Get platform usage service."""
    return get_platform_usage()
