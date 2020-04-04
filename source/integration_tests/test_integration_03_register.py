"""Integration test for signup."""
import pytest

from funwithflags.definitions import RegisterRequest
from funwithflags.use_cases import register

from .conftest import LOGIN_USER


@pytest.mark.usefixtures("context")
def test_register(context):
    # Given
    request = RegisterRequest(
        username=LOGIN_USER.username,
        nickname=LOGIN_USER.nickname,
        email=LOGIN_USER.email,
        password=LOGIN_USER.password,
    )
    # When
    result = register(request, context)
    # Then
    assert isinstance(result, int)
    assert result > 0
