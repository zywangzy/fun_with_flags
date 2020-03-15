"""Integration test for login."""
import pytest

import flask_jwt_simple

from funwithflags.definitions import LoginRequest, BadRequestError, DatabaseQueryError
from funwithflags.use_cases import login

from .conftest import LOGIN_USER


@pytest.mark.usefixtures("context")
def test_login(monkeypatch, context):
    # Given
    expected_username = LOGIN_USER.username
    request = LoginRequest(
        username=expected_username,
        password="Password123@"
    )
    expected_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."\
                     "eyJleHAiOjE1ODM5MTIzMTAsImlhdCI6MTU4MzkwODcxMCwibmJmIjoxNTgzOTA4NzEwLCJzdWIiOjF9."\
                     "eilQgqIePisy1bURTtPjJNBR74VrWpun6H0ET6r1Quk"

    # Monkeypatch flask_jwt_simple
    def mock_create_jwt(identity):
        return expected_token

    monkeypatch.setattr(flask_jwt_simple, 'create_jwt', mock_create_jwt)

    # When
    username, token = login(request, context)
    # Then
    assert username == expected_username
    assert token == expected_token


@pytest.mark.usefixtures("context")
def test_login_user_not_found_failure(context):
    # Given
    request = LoginRequest(
        username="noSuchUser",  # Non-existent
        password="password"
    )
    # When & Then
    with pytest.raises(DatabaseQueryError):
        login(request, context)


@pytest.mark.usefixtures("context")
def test_login_wrong_password_failure(context):
    # Given
    request = LoginRequest(
        username=LOGIN_USER.username,
        password="wrongPassword"
    )
    # When & Then
    with pytest.raises(BadRequestError):
        login(request, context)
