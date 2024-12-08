# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

import logging

import importlib_metadata


logger = logging.getLogger(__name__)


ADDONS = {}


for entry in importlib_metadata.entry_points(group="datalayer_iam.addons_credits_v1"):
    ADDONS[entry.name] = entry
