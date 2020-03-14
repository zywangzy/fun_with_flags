from datetime import datetime
import pytest
import tempfile

from funwithflags.definitions import User
from funwithflags.gateways import Context, make_postgres_gateway


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
    password=b"123456",
    salt=b"123",
    created_at=CREATE_TIME,
    valid=True,
)


class TestUser:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


LOGIN_USER = TestUser(
    username="testUser",
    nickname="testAcct",
    email="testUser@example.com",
    password="Password123@",
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
    return Context(postgres_gateway=pg_gateway)
