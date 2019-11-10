"""Module for the Postgres database gateway."""
from configparser import ConfigParser
from typing import Mapping

import psycopg2

from .db_gateway_abc import DbGateway


class PostgresGateway(DbGateway):
    def __init__(self,
                 host: str,
                 port: int,
                 dbname: str,
                 user: str,
                 password: str):
        self._conn_str = f"host={host} port={port} dbname={dbname} user={user} password={password}"
        self._conn = psycopg2.connect(self._conn_str)


def make_postgres_gateway() -> PostgresGateway:
    """Factory method to create a `PostgresGateway` object."""
    def read_postgres_config(filename='database.ini', section='postgresql') -> Mapping[str, str]:
        """Read configuration file and return a dictionary mapping from field name to field value."""
        parser = ConfigParser()
        parser.read(filename)
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(f"{filename} does not have section {section}.")
        return db
    config = read_postgres_config()
    return PostgresGateway(host=config['host'],
                           port=int(config['port']),
                           dbname=config['dbname'],
                           user=config['user'],
                           password=config['password'])
