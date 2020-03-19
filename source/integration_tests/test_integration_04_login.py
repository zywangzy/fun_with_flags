"""Integration test for login."""
import pytest

import flask_jwt_extended

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
    expected_access_token = "expected.Access.Token"
    expected_refresh_token = "expected.Refresh.Token"
    expected_access_jti = "expected.Access.Jti"
    expected_refresh_jti = "expected.Refresh.Jti"

    # Monkeypatch flask_jwt_extended
    def mock_create_access_token(identity, fresh):
        return expected_access_token

    def mock_create_refresh_token(identity):
        return expected_refresh_token

    def mock_get_jti(encoded_token):
        if encoded_token == expected_access_token:
            return expected_access_jti
        elif encoded_token == expected_refresh_token:
            return expected_refresh_jti

    monkeypatch.setattr(flask_jwt_extended, 'create_access_token', mock_create_access_token)
    monkeypatch.setattr(flask_jwt_extended, 'create_refresh_token', mock_create_refresh_token)
    monkeypatch.setattr(flask_jwt_extended, 'get_jti', mock_get_jti)

    # When
    username, access_token, refresh_token = login(request, context)
    cache_access_value = context.redis_gateway.get(expected_access_jti)
    cache_refresh_value = context.redis_gateway.get(expected_refresh_jti)

    # Then
    assert username == expected_username
    assert access_token == expected_access_token
    assert refresh_token == expected_refresh_token
    assert cache_access_value and cache_access_value == "login"
    assert cache_refresh_value and cache_refresh_value == "login"


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
