# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

import json
from unittest import mock

import pytest
pytest.importorskip("jupyter_server")

from datalayer_iam.jupyter import DATALAYER_AUTHENTICATION_HEADER, DatalayerProvider

pytest_plugins = ["jupyter_server.pytest_plugin"]


async def test_DatalayerProvider(tester, client, jp_serverapp, jp_fetch):
    tester_handle, _ = tester
    idp = DatalayerProvider(
        parent=jp_serverapp,
    )
    assert idp.auth_enabled

    with mock.patch.dict(jp_serverapp.web_app.settings, {"user_provider": idp}):
        resp = await jp_fetch("/api/me", headers={DATALAYER_AUTHENTICATION_HEADER: f"bearer {client.jwt_token}", "Cookie": ""})

        user_info = json.loads(resp.body.decode("utf8"))
        assert user_info["user"]["username"] == tester_handle
        # We don't use a cookie
        assert "Set-Cookie" not in resp.headers
