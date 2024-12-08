# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

import logging

from connexion.exceptions import OAuthProblem

from datalayer_common.authn import authn # This import is needed, do not remove it.
from datalayer_common.authn.key import create_user_for_key
from datalayer_common.config import IAM_API_KEY


logger = logging.getLogger(__name__)


def api_key_auth(key, required_scopes):
    """Authentication for API call between services."""
    if IAM_API_KEY and key != IAM_API_KEY:
        raise OAuthProblem(f"Invalid key provided - Key value not shared for security reasons...")

    return create_user_for_key(key)
