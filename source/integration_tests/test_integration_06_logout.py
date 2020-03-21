"""Integration test for logout."""
import pytest

import flask_jwt_extended

from funwithflags.definitions import LogoutRequest
from funwithflags.use_cases import logout


@pytest.mark.usefixtures("context")
def test_logout(context):
    # Given
    jti = "fake.jti"
    expected_status = "logout"

    # When
    logout(LogoutRequest(jti), context)

    # Then
    status = context.redis_gateway.get(jti)
    assert status and expected_status == status
