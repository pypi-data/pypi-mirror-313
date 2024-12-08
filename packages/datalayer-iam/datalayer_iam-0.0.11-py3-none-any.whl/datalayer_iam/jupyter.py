# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""Jupyter Server auth providers based on Datalayer IAM."""

from __future__ import annotations

import logging
from typing import Optional

from datalayer_common.authn import decode_jwt_token
from werkzeug.exceptions import Unauthorized

try:
    from jupyter_server.auth import IdentityProvider, User
except ImportError:
    IdentityProvider = None


logger = logging.getLogger(__name__)


# Custom header transporting a JWT token
DATALAYER_AUTHENTICATION_HEADER = "X-Datalayer-Authorization"

# Make jupyter server only a optional dependency
if IdentityProvider is not None:
    from tornado.web import RequestHandler

    class DatalayerProvider(IdentityProvider):
        token = ""
        need_token = False
        
        def get_user(self, handler: RequestHandler) -> Optional[User]:
            user_token = ""
            m = self.auth_header_pat.match(
                handler.request.headers.get(DATALAYER_AUTHENTICATION_HEADER, "")
            )
            if m:
                user_token = m.group(2)
            if not user_token:
                user_token = handler.get_argument("token", "")
            
            try:
                token = decode_jwt_token(user_token)
            except Unauthorized as e:
                logger.info("Invalid token", exc_info=e)
                return None
            else:
                handle = token["sub"]
                if isinstance(handle, str):
                    return User(handle)
                else:
                    return User(
                        handle["handle"],
                        handle["handle"],
                        f"{handle.get('first_name', '')} {handle.get('last_name', '')}".strip(),
                        f"{handle.get('first_name', ' ')[0]}{handle.get('last_name', ' ')[0]}".strip()
                        or None,
                    )
