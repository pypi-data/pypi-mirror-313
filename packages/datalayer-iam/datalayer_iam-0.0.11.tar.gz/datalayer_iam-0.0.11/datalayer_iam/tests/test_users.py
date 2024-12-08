# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

import pytest

from .conftest import BASE_URL, DEFAULT_HANDLE


def test_default_user(client):
    response = client.get(f"{BASE_URL}/user")
    data = response.json()
    assert data["success"]
    assert data["profile"]["roles_ss"] == ["user"]


def test_add_role(client, tester, user_factory, client_factory):
    admin_connection = user_factory("admin")

    response = client_factory(*admin_connection).put(
        f"{BASE_URL}/user/{DEFAULT_HANDLE}/role", json={"role": "admin"}
    )
    data = response.json()
    assert data["success"]

    # Check the user token was revoked
    r = client.get(f"{BASE_URL}/me")
    assert r.status_code == 401

    response = client_factory(*tester).get(f"{BASE_URL}/me")
    data = response.json()
    assert data["success"]
    assert "admin" in data["me"]["roles"]


def test_remove_role(tester, client, user_factory, client_factory):
    admin_connection = user_factory("admin")
    admin_client = client_factory(*admin_connection)
    role = "dummy"
    response = admin_client.put(
        f"{BASE_URL}/user/{DEFAULT_HANDLE}/role", json={"role": role}
    )

    response = admin_client.delete(f"{BASE_URL}/user/{DEFAULT_HANDLE}/role/{role}")
    data = response.json()
    assert data["success"]

    # Check the token was revoked
    r = client.get(f"{BASE_URL}/me")
    assert r.status_code == 401

    response = client_factory(*tester).get(f"{BASE_URL}/me")
    data = response.json()
    assert data["success"]
    assert role not in data["me"]["roles"]


@pytest.mark.parametrize("role,expected", (("user", True), ("banana", False)))
def test_check_role(client, role, expected):
    response = client.get(f"{BASE_URL}/user/{DEFAULT_HANDLE}/role/{role}")
    data = response.json()
    assert data["success"] is expected
