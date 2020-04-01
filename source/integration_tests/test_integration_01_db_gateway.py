"""Integration test for database gateway."""
import pytest

from funwithflags.definitions import User
from funwithflags.definitions import BadRequestError, DatabaseQueryError

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
    "user_id_name,expected",
    [(1, EXAMPLE_USER), (EXAMPLE_USER.username, EXAMPLE_USER)]
)
def test_postgres_gateway_read_user(pg_gateway, user_id_name, expected):
    # When
    user = pg_gateway.read_user(user_id=user_id_name) if isinstance(user_id_name, int) else \
        pg_gateway.read_user(username=user_id_name)
    # Then
    assert compare_users_without_created_at(expected, user)


@pytest.mark.usefixtures("pg_gateway")
@pytest.mark.parametrize(
    "user_id_name,exception",
    [(-1, BadRequestError), (0, BadRequestError), (100, DatabaseQueryError), ("NotExist", DatabaseQueryError)]
)
def test_postgres_gateway_read_user_failure(pg_gateway, user_id_name, exception):
    # When & Then
    with pytest.raises(exception):
        if isinstance(user_id_name, int):
            pg_gateway.read_user(user_id=user_id_name)
        else:
            pg_gateway.read_user(username=user_id_name)


@pytest.mark.usefixtures("pg_gateway")
@pytest.mark.parametrize(
    "user_id,kwargs,expected",
    [
        (
            1,
            {"username": "newtest", "password": b"654321", "salt": b"321"},
            (
                None,
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
    "user_id, kwargs, exception",
    [(0, {}, BadRequestError),
     (1, {}, BadRequestError),
     (1, {"InvalidField": "abc"}, BadRequestError),
     (100, {"username": "aUser"}, DatabaseQueryError)]
)
def test_postgres_gateway_update_user_failure(pg_gateway, user_id, kwargs, exception):
    # When & Then
    with pytest.raises(exception):
        pg_gateway.update_user(user_id, **kwargs)


@pytest.mark.usefixtures("pg_gateway")
def test_postgres_gateway_delete_user(pg_gateway):
    # When
    user_id = 1
    result = pg_gateway.delete_user(user_id)
    # Then
    assert result is None


@pytest.mark.usefixtures("pg_gateway")
@pytest.mark.parametrize(
    "user_id,exception", [(-1, BadRequestError), (0, BadRequestError), (2, DatabaseQueryError)]
)
def test_postgres_gateway_delete_user_failure(pg_gateway, user_id, exception):
    # When & Then
    with pytest.raises(exception):
        pg_gateway.delete_user(user_id)
