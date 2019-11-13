"""Integration test for database gateway."""
from datetime import datetime
import pytest
import tempfile

from funwithflags.definitions import User
from funwithflags.gateways.db_gateway import (
    make_postgres_gateway,
    # PostgresGateway,
)

DATABASE_CONFIG = """[postgresql]
host=dbpostgres
port=5432
dbname=postgres
user=service
password=password
"""
CREATE_TIME = datetime.now()


@pytest.fixture
def pg_gateway():
    with tempfile.NamedTemporaryFile(mode="w+t", suffix=".ini") as temp_file:
        temp_file.write(DATABASE_CONFIG)
        temp_file.seek(0)
        return make_postgres_gateway(temp_file.name)


@pytest.fixture
def example_user():
    return User(
        user_id=1,
        username="test",
        nickname="nick",
        email="test@example.com",
        password=bytearray(b"123456"),
        salt=bytearray(b"123"),
        created_at=CREATE_TIME,
        valid=True,
    )


def test_make_postgres_gateway(pg_gateway):
    # Then
    assert pg_gateway is not None


def test_postgres_gateway_create_user(pg_gateway, example_user):
    # Expected
    expected_user_id = example_user.user_id
    # When
    user_id = pg_gateway.create_user(example_user)
    # Then
    assert expected_user_id == user_id


def test_postgres_gateway_read_user(pg_gateway, example_user):
    # Expected
    expected_user = example_user
    # When
    user = pg_gateway.read_user(example_user.user_id)
    # Then
    assert expected_user == user
