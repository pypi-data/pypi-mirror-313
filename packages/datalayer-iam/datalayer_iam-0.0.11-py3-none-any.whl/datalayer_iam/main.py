# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""Datalayer IAM application."""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import sys
import typing
from http import HTTPStatus
from urllib.parse import quote

from connexion import AsyncApp, ConnexionMiddleware
from connexion.lifecycle import ConnexionRequest, ConnexionResponse
from connexion.resolver import RelativeResolver
from connexion.middleware import MiddlewarePosition
from pysolr import SolrError
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse
from werkzeug.exceptions import HTTPException

from datalayer_common.authz.middleware import AuthzMiddleware
from datalayer_common.config import (
    AUTHZ_ENGINE,
    JWT_SECRET,
    RUNTIME_ENV,
)
from datalayer_common.instrumentation import instrument
from datalayer_iam.addons import ADDONS
from datalayer_iam.addons.test import TestAddon
from datalayer_iam.config import (
    CREDITS_PROVIDER,
    ROOT_FOLDER,
)
from datalayer_iam.messaging import listen_usage_messages
from datalayer_iam.services.accounts import get_credits_customer_id_service
from datalayer_iam.services.credits import set_account_credits_service
from datalayer_addons.credits import ABCCreditsAddon
from datalayer_solr import DATALAYER_FAVICO


PORT = 9700


logging.getLogger("pysolr").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


PASSWORD_MIN_LENGTH = 6
PASSWORD_MAX_LENGTH = 30

MAIL_REGEXP = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


credit_addon = None

_variant = ADDONS.get(CREDITS_PROVIDER)
if _variant is None:
    logger.critical("Not a valid addon provider: %s", CREDITS_PROVIDER)
else:
    try:
        credit_addon = _variant.load()()
        logger.info("Addon [%s] is loaded.", CREDITS_PROVIDER)
    except BaseException as e:
        logger.error(f"Failed to load addon {CREDITS_PROVIDER}.", exc_info=e)

# Inject helper that interact with the DB.
ABCCreditsAddon.get_credits_customer_id = get_credits_customer_id_service
ABCCreditsAddon.set_account_credits = set_account_credits_service
credit_addon = credit_addon or (
    TestAddon() if RUNTIME_ENV == "dev" else ABCCreditsAddon()
)


async def init_openfga_engine():
    """Call this if you are using OpenFGA as Authz."""
    from datalayer_common.authz.openfga import init_openfga

    await init_openfga()


# Callback to shutdown instrumentation resources
shutdown = None


@contextlib.asynccontextmanager
async def initialize_iam(app: ConnexionMiddleware) -> typing.AsyncIterator:
    if JWT_SECRET is None:
        logger.error("😱 A valid JWT secret must be provided.")
        sys.exit(1)

    if AUTHZ_ENGINE == "openfga":
        await init_openfga_engine()
    elif AUTHZ_ENGINE == "none":
        logger.warning(
            "😱 Running without authorizer in environment [%s].", RUNTIME_ENV
        )

    task = asyncio.create_task(listen_usage_messages(credit_addon))
    try:
        yield {"addon": credit_addon}
    finally:
        if shutdown is not None:
            shutdown()
        task.cancel()
        await task


app = AsyncApp(__name__, lifespan=initialize_iam)

app.add_middleware(
    CORSMiddleware,
    position=MiddlewarePosition.BEFORE_EXCEPTION,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_api(
    str(ROOT_FOLDER.joinpath("api", "v1", "openapi.yml")),
    resolver=RelativeResolver("datalayer_iam.api.v1"),
)

addon_routes = credit_addon.get_routes()
if addon_routes is not None:
    logger.info("Adding addon routes.")
    app.add_api(addon_routes[0], resolver=RelativeResolver(addon_routes[1]))


# Public catch all routes.


@app.route("/api/iam/version", methods=["GET"])
def index_endpoint(*args, **kwargs):
    """Catch all route showing the version."""
    icon = ROOT_FOLDER / "res" / "iam.svg"
    return HTMLResponse(
        f"""<html>
  <head>
    <title>Datalayer IAM Ξ Accelerated and Trusted Jupyter</title>
    <link rel="shortcut icon" href="{DATALAYER_FAVICO}" type="image/x-icon">
  </head>
  <body>
    <h1>Datalayer IAM</h1>
    <img src="data:image/svg+xml,{quote(icon.read_bytes())}" width="200" />
  </body>
</html>
"""
    )


# Catch All Exceptions.


def all_exception_handler(
    request: ConnexionRequest, exception: Exception
) -> ConnexionResponse:
    """All Exception handler."""
    logger.error("Request failed", exc_info=exception)
    code = (
        exception.code
        if isinstance(exception, HTTPException)
        else HTTPStatus.INTERNAL_SERVER_ERROR
    )
    return ConnexionResponse(
        status_code=code,
        body=json.dumps(
            {
                "success": False,
                "message": "Server Error.",
                "exception": "Database Request Error."
                if isinstance(exception, SolrError)
                else repr(exception),
            }
        ),
    )


app.add_error_handler(Exception, all_exception_handler)


# Instrument the application
shutdown = instrument(app, "iam")

app.add_middleware(AuthzMiddleware)

# Main.


def main():
    """Main method."""
    logger.info(
        "Server listening on port [%s] - Browse http://localhost:%s", PORT, PORT
    )
    app.run(
        host="0.0.0.0",
        port=PORT,
        lifespan="on",  # Activate to crash the server when loading spec with errors.
    )


if __name__ == "__main__":
    main()
