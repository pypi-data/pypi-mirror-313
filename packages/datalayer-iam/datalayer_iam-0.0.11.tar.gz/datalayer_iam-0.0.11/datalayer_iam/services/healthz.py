# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""Healthz service."""

from datalayer_solr.healthz import ping_solr


def ping_service():
    """Ping healtz service."""
    return ping_solr()
