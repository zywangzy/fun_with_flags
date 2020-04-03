"""Integration test for fresh login."""
import pytest

import flask_jwt_extended

from funwithflags.definitions import FreshLoginRequest, BadRequestError, DatabaseQueryError
from funwithflags.use_cases import fresh_login

from .conftest import LOGIN_USER

LOGIN_USER_ID = 0


@pytest.fixture
def get_user_id(context):
    global LOGIN_USER_ID
    if LOGIN_USER_ID == 0:
        LOGIN_USER_ID = context.postgres_gateway.read_user(username=LOGIN_USER.username).user_id


@pytest.mark.usefixtures("context")
def test_fresh_login(monkeypatch, get_user_id, context):
    # Given
    request = FreshLoginRequest(
        user_id=LOGIN_USER_ID,
        password="Password123@"
    )
    expected_access_token = "expected.Access.Token"
    expected_access_jti = "expected.Access.Jti"

    # Monkeypatch flask_jwt_extended
    def mock_create_access_token(identity, fresh):
        return expected_access_token

    def mock_get_jti(encoded_token):
        return expected_access_jti

    monkeypatch.setattr(flask_jwt_extended, 'create_access_token', mock_create_access_token)
    monkeypatch.setattr(flask_jwt_extended, 'get_jti', mock_get_jti)

    # When
    access_token = fresh_login(request, context)
    cache_access_value = context.redis_gateway.get(expected_access_jti)

    # Then
    assert access_token == expected_access_token
    assert cache_access_value and cache_access_value == "login"


@pytest.mark.usefixtures("context")
def test_login_user_not_found_failure(context):
    # Given
    request = FreshLoginRequest(
        user_id=1000,  # Non-existent
        password="password"
    )
    # When & Then
    with pytest.raises(DatabaseQueryError):
        fresh_login(request, context)


@pytest.mark.usefixtures("context")
def test_login_wrong_password_failure(get_user_id, context):
    # Given
    request = FreshLoginRequest(
        user_id=LOGIN_USER_ID,
        password="wrongPassword"
    )
    # When & Then
    with pytest.raises(BadRequestError):
        fresh_login(request, context)
