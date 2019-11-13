"""Module for the Postgres database gateway."""
from configparser import ConfigParser
from datetime import datetime
import logging
from time import sleep
from typing import Any, List, Mapping

import psycopg2

from .db_gateway_abc import DbGateway
from funwithflags.definitions import User
from funwithflags.entities.db_util import read_postgres_config


logger = logging.getLogger(__name__)


class PostgresGateway(DbGateway):
    def __init__(self,
                 host: str,
                 port: int,
                 dbname: str,
                 user: str,
                 password: str):
        self._conn_str = f"host={host} port={port} dbname={dbname} user={user} password={password}"
        self._conn_retry_limit = 20
        self._conn_retry_interval = 2
        self._active = False

        retry = 0
        for _ in range(self._conn_retry_limit):
            try:
                retry += 1
                self._conn = psycopg2.connect(self._conn_str)
            except Exception as e:
                logger.info(f"PostgresGateway connection failed, will retry for #{retry} "
                            f"in {self._conn_retry_interval} seconds. Error: {e}")
                sleep(self._conn_retry_interval)
                continue
            else:
                self._active = True
                break
        if not self._active:
            logger.error(f"PostgresGateway connection failed after {retry} times, stopping retry.")
            raise Exception("PostgresGateway connection failure after retries.")
        else:
            logger.info("PostgresGateway connection success!")

    def __del__(self):
        """Destructor.
        """
        if self._active:
            self.deactivate()

    def deactivate(self):
        """Deactivate the gateway. Close the connection.
        """
        self._active = False
        self._conn.close()

    def query(self, query: str, *args) -> Any:
        """Given a `query` string, do the query and return result.
        """
        try:
            cur = self._conn.cursor()
            cur.execute(query, args)
            result = cur.fetchone()
            self._conn.commit()
            cur.close()
            return result
        except (Exception, psycopg2.DatabaseError) as e:
            logger.error(f"PostgresGateway failed on query: '{query}' with {args}.")
            return None

    def create_user(self, user: User) -> int:
        """Given a `user` object, create user entry in database table and return
        an integer of `user_id` of created user.
        """
        query = """INSERT INTO users(username, nickname, email, password, salt, created_at) 
                   VALUES (%s, %s, %s, %s, %s, %s) RETURNING user_id"""
        user_id = self.query(query,
                             user.username,
                             user.nickname,
                             user.email,
                             user.password,
                             user.salt,
                             user.created_at)
        return user_id[0] if user_id is not None and len(user_id) == 1 else -1

    def read_user(self, user_id: int) -> User:
        """Given a `user_id` integer, read user info from database and return a
        `User` object.
        """
        query = """SELECT * FROM users WHERE user_id = %s"""
        result = self.query(query, user_id)
        if result is None:
            return User(valid=False)
        return User(user_id=result[0],
                    username=result[1],
                    nickname=result[2],
                    password=bytearray(result[3]),
                    salt=bytearray(result[4]),
                    email=result[5],
                    created_at=result[6],
                    valid=True)


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
