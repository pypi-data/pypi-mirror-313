# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""Configuration."""

import os
from pathlib import Path

import datalayer_iam


ROOT_FOLDER = (
    Path(os.curdir).joinpath("data").resolve()
    # Trick to know if the package was processed by Nuitka or not.
    if hasattr(datalayer_iam, "__compiled__")
    else Path(__file__).resolve().parent
)

#####################################################################
# GitHub
#####################################################################

DATALAYER_GITHUB_CLIENT_ID = os.environ.get("DATALAYER_GITHUB_CLIENT_ID", "")
DATALAYER_GITHUB_CLIENT_SECRET = os.environ.get("DATALAYER_GITHUB_CLIENT_SECRET", "")

#####################################################################
# LinkedIn
#####################################################################

DATALAYER_LINKEDIN_CLIENT_ID = os.environ.get("DATALAYER_LINKEDIN_CLIENT_ID", "")
DATALAYER_LINKEDIN_CLIENT_SECRET = os.environ.get("DATALAYER_LINKEDIN_CLIENT_SECRET", "")

#####################################################################
# X
#####################################################################

DATALAYER_X_API_KEY = os.environ.get("DATALAYER_X_API_KEY", "")
DATALAYER_X_API_SECRET = os.environ.get("DATALAYER_X_API_SECRET", "")

#####################################################################
# Credits
#####################################################################

INITIAL_USER_CREDITS = int(os.environ.get("DATALAYER_INITIAL_USER_CREDITS", "100"))

#####################################################################
# Addons
#####################################################################

CREDITS_PROVIDER = os.environ.get("DATALAYER_CREDITS_PROVIDER", "")
