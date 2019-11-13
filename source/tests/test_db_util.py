import pytest
import tempfile

from funwithflags.gateways.db_gateway import (
    read_postgres_config,
)


DATABASE_CONFIG = """[postgresql]
host=dbpostgres
port=5432
dbname=postgres
user=service
password=password
"""


def test_read_postgres_config():
    with tempfile.NamedTemporaryFile(mode="w+t", suffix=".ini") as temp_file:
        # Given
        expected_config = {
            "host": "dbpostgres",
            "port": "5432",
            "dbname": "postgres",
            "user": "service",
            "password": "password",
        }
        temp_file.write(DATABASE_CONFIG)
        temp_file.seek(0)

        # When
        config = read_postgres_config(temp_file.name)

        # Then
        assert expected_config == config