"""Integration test for logout."""
import pytest

import flask_jwt_extended

from funwithflags.definitions import LogoutRequest
from funwithflags.use_cases import logout


@pytest.mark.usefixtures("context")
def test_logout(monkeypatch, context):
    # Given
    refresh_token = "token"
    expected_jti = "fake.jti"
    expected_status = "logout"

    def mock_get_jti(encoded_token):
        return expected_jti

    monkeypatch.setattr(flask_jwt_extended, 'get_jti', mock_get_jti)

    # When
    logout(LogoutRequest(1, refresh_token), context)

    # Then
    status = context.redis_gateway.get(expected_jti)
    assert status and expected_status == status
