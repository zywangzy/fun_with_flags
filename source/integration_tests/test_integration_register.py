"""Integration test for signup."""
import json
import pytest

from funwithflags.definitions import RegisterRequest
from funwithflags.use_cases import register


@pytest.mark.usefixtures("context")
def test_register(context):
    # Given
    request = RegisterRequest(
        username="testuser",
        nickname="usr123",
        email="test@test.com",
        password="Password123@",
    )
    # When
    result = register(request, context)
    # Then
    assert isinstance(result, int)
    assert result > 0
