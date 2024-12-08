# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

from __future__ import annotations

import secrets
from functools import partial
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    import starlette

from datalayer_iam.main import app


BASE_URL = "/api/iam/v1"

DEFAULT_HANDLE = "pytester"


@pytest.fixture
def user_factory(request):
    def g(handle: str) -> tuple[str, str]:
        password = secrets.token_hex()[:20]
        with app.test_client() as client:
            r = client.post(
                f"{BASE_URL}/join/request",
                json={
                    "handle": handle,
                    "email": "pytester@datalayer.io",
                    "firstName": "Py",
                    "lastName": "Tester",
                    "password": password,
                    "passwordConfirm": password,
                },
            )
            data = r.json()
            assert data["success"]
            token = data["token"]
            r = client.get(f"{BASE_URL}/join/confirm/user/{data['user_handle']}/{token}")
            data2 = r.json()
            assert data2["success"]

            def teardown(password):
                if password:
                    r = client.post(
                        f"{BASE_URL}/login",
                        json={"handle": handle, "password": password},
                    )
                    token = r.json()["token"]
                    client.delete(
                        f"{BASE_URL}/me", headers={"Authorization": f"Bearer {token}"}
                    )

            # Generator does not work with factory fixture
            request.addfinalizer(partial(teardown, password))
            return handle, password

    return g


@pytest.fixture
def tester(user_factory):
    return user_factory(DEFAULT_HANDLE)


@pytest.fixture
def client_factory():
    def f(handle: str, password: str) -> starlette.testclient.TestClient:
        # Generate a new token for every test as we use a very small expiration time
        with app.test_client() as client:
            r = client.post(
                f"{BASE_URL}/login",
                json={"handle": handle, "password": password},
            )
            token = r.json()["token"]

        with app.test_client(headers={"Authorization": f"Bearer {token}"}) as client:
            client.jwt_token = token
            return client

    return f


@pytest.fixture
def client(tester, client_factory):
    return client_factory(*tester)
