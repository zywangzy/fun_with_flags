"""Integration test for refresh access token."""
import pytest

import flask_jwt_extended

from funwithflags.use_cases import refresh_access_token


@pytest.mark.usefixtures("context")
def test_refresh_access_token(monkeypatch, context):
    # Given
    expected_access_token = "fake.Access.Token"
    expected_jti = "new.Token"
    expected_status = "login"

    # Monkeypatch flask_jwt_extended

    def mock_create_access_token(identity):
        return expected_access_token

    def mock_get_jti(encoded_token):
        return expected_jti

    monkeypatch.setattr(flask_jwt_extended, 'create_access_token', mock_create_access_token)
    monkeypatch.setattr(flask_jwt_extended, 'get_jti', mock_get_jti)

    # When
    new_token = refresh_access_token(identity=10, context=context)
    status = context.redis_gateway.get(expected_jti)

    # Then
    assert expected_access_token == new_token
    assert expected_status == status
