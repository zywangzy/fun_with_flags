"""Integration test for database gateway."""
import pytest

from funwithflags.definitions import User
from funwithflags.definitions import DatabaseQueryError

from .conftest import CREATE_TIME, EXAMPLE_USER


def compare_users_without_created_at(user1: User, user2: User):
    return (
        user1.user_id == user2.user_id
        and user1.username == user2.username
        and user1.nickname == user2.nickname
        and user1.email == user2.email
        and user1.password == user2.password
        and user1.salt == user2.salt
        and user1.valid == user2.valid
    )


@pytest.mark.usefixtures("pg_gateway")
def test_make_postgres_gateway(pg_gateway):
    # Then
    assert pg_gateway is not None


@pytest.mark.usefixtures("pg_gateway")
def test_postgres_gateway_create_user_success(pg_gateway):
    """Success for the first time.
    """
    # Given
    user = EXAMPLE_USER
    expected_user_id = 1
    # When
    user_id = pg_gateway.create_user(user)
    # Then
    assert expected_user_id == user_id


@pytest.mark.usefixtures("pg_gateway")
def test_postgres_gateway_create_user_failure(pg_gateway):
    """When creating user with duplicate info, query should fail and raise exception.
    """
    # Given
    user = EXAMPLE_USER
    # When & Then
    with pytest.raises(DatabaseQueryError):
        pg_gateway.create_user(user)


@pytest.mark.usefixtures("pg_gateway")
@pytest.mark.parametrize(
    "user_id,expected", [(-1, User()), (0, User()), (1, EXAMPLE_USER)]
)
def test_postgres_gateway_read_user(pg_gateway, user_id, expected):
    # When
    user = pg_gateway.read_user(user_id)
    # Then
    assert compare_users_without_created_at(expected, user)


@pytest.mark.usefixtures("pg_gateway")
@pytest.mark.parametrize(
    "user_id,kwargs,expected",
    [
        (0, {}, (False, User())),
        (
            1,
            {"username": "newtest", "password": b"654321", "salt": b"321",},
            (
                True,
                User(
                    user_id=1,
                    username="newtest",
                    nickname="nick",
                    email="test@example.com",
                    password=b"654321",
                    salt=b"123",
                    created_at=CREATE_TIME,
                    valid=True,
                ),
            ),
        ),
    ],
)
def test_postgres_gateway_update_user(pg_gateway, user_id, kwargs, expected):
    # When
    update_result = pg_gateway.update_user(user_id, **kwargs)
    user = pg_gateway.read_user(user_id)
    # Then
    assert expected == (update_result, user)


@pytest.mark.usefixtures("pg_gateway")
@pytest.mark.parametrize(
    "user_id,expected", [(-1, False), (0, False), (1, True), (2, False)]
)
def test_postgres_gateway_delete_user(pg_gateway, user_id, expected):
    # When
    result = pg_gateway.delete_user(user_id)
    # Then
    assert expected == result
