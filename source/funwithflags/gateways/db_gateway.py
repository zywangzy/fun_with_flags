"""Module for the Postgres database gateway."""
from configparser import ConfigParser
import logging
from typing import List, Mapping

import psycopg2

from .db_gateway_abc import DbGateway
from funwithflags.definitions import User


logger = logging.getLogger(__name__)


class PostgresGateway(DbGateway):
    def __init__(self,
                 host: str,
                 port: int,
                 dbname: str,
                 user: str,
                 password: str):
        self._conn_str = f"host={host} port={port} dbname={dbname} user={user} password={password}"
        self._conn = psycopg2.connect(self._conn_str)

    def query(self, command: str) -> List:
        """Given a `command` string, do the query and return a list of results.
        """
        return []

    def create_user(self, user: User) -> int:
        """Given a `user` object, create user entry in database table and return
        an integer of `user_id` of created user.
        """
        return 0

    def read_user(self, user_id: int) -> User:
        """Given a `user_id` integer, read user info from database and return a
        `User` object.
        """
        return User()


def read_postgres_config(filename='database.ini', section='postgresql') -> Mapping[str, str]:
    """Read configuration file and return a dictionary mapping from field name to field value."""
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    # print(parser.sections())
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f"{filename} does not have section {section}, sections are {parser.sections()}")
    return db


def make_postgres_gateway(filename='database.ini') -> PostgresGateway:
    """Factory method to create a `PostgresGateway` object."""
    try:
        config = read_postgres_config(filename)
        return PostgresGateway(host=config['host'],
                               port=int(config['port']),
                               dbname=config['dbname'],
                               user=config['user'],
                               password=config['password'])
    except KeyError as e:
        logger.error(f"Invalid database config file: {e}")
        raise e
    except Exception as e:
        logger.error(f"Failed to initialize PostgresGateway: {e}")
        raise e
