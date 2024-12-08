# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""Datalayer Accounts service."""

from datalayer_solr.accounts import get_account_by_handle, get_account_by_uid


def get_account_by_handle_service(account_handle, public=True):
    """Get an account by handle."""
    return get_account_by_handle(account_handle, public)


def get_account_by_uid_service(account_uid: str, public: bool=True) -> dict:
    """Get an account by uid."""
    return get_account_by_uid(account_uid, public)


def get_credits_customer_id_service(account_uid: str) -> str | None:
    """Get the customer ID for an account."""
    return get_account_by_uid_service(account_uid, False).get("credits_customer_uid")
