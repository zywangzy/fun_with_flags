"""Integration test for signup."""
import json
import pytest

from funwithflags.definitions import SignupRequest
from funwithflags.use_cases import signup


@pytest.mark.usefixtures("context")
def test_signup(context):
    # Given
    request = SignupRequest(username="testuser", nickname="usr123", email="test@test.com", password="password")
    # When
    result = signup(request, context)
    # Then
    assert isinstance(result, int)
    assert result != -1
    assert result > 0
