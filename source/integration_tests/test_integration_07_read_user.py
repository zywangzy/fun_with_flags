"""Integration test for reading user."""
import pytest

from funwithflags.definitions import BadRequestError, DatabaseQueryError
from funwithflags.use_cases import read_user_basic

from .conftest import CREATE_TIME, EXAMPLE_USER

user_id = 0


@pytest.fixture
def create_user(context):
    global user_id
    user_id = context.postgres_gateway.create_user(EXAMPLE_USER)


def test_read_user_basic(create_user, context):
    # Given
    expected_user_id = user_id
    # When
    result = read_user_basic(user_id=expected_user_id, context=context)
    # Then
    assert len(result) == 5
    assert result["userid"] == expected_user_id
    assert result["username"] == EXAMPLE_USER.username
    assert result["nickname"] == EXAMPLE_USER.nickname
    assert result["email"] == EXAMPLE_USER.email
    assert result["created_at"] == str(CREATE_TIME)


@pytest.mark.parametrize(
    "user_id,exception",
    [(-1, BadRequestError),
     (0, BadRequestError),
     (1, DatabaseQueryError)]
)
def test_read_user_basic_failure(context, user_id, exception):
    # When & Then
    with pytest.raises(exception):
        read_user_basic(user_id=user_id, context=context)
