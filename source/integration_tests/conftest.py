from datetime import datetime
import pytest
import tempfile

from funwithflags.definitions import User
from funwithflags.gateways import make_postgres_gateway, make_context


"""Test variables."""
DATABASE_CONFIG = """[postgresql]
host=dbpostgres
port=5432
dbname=postgres
user=service
password=password
"""
CREATE_TIME = datetime.now()
EXAMPLE_USER = User(
    user_id=1,
    username="test",
    nickname="nick",
    email="test@example.com",
    password=bytearray(b"123456"),
    salt=bytearray(b"123"),
    created_at=CREATE_TIME,
    valid=True,
)


@pytest.fixture
def pg_gateway():
    with tempfile.NamedTemporaryFile(mode="w+t", suffix=".ini") as temp_file:
        temp_file.write(DATABASE_CONFIG)
        temp_file.seek(0)
        return make_postgres_gateway(temp_file.name)


@pytest.fixture
@pytest.mark.usefixtures("pg_gateway")
def context(pg_gateway):
    return make_context(pg_gateway)
