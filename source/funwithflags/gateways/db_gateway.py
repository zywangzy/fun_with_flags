"""Module for the Postgres database gateway."""
import logging
from time import sleep
from typing import Any

import psycopg2

from .db_gateway_abc import DbGateway
from funwithflags.definitions import DatabaseQueryError, User
from funwithflags.entities import generate_update_params, read_postgres_config


logger = logging.getLogger(__name__)


class PostgresGateway(DbGateway):
    def __init__(self, host: str, port: int, dbname: str, user: str, password: str):
        """Constructor. Try to connect to Postgres database with given parameters. Will retry after connection failure
        for up to 20 times, each time wait for 2 seconds. Raises an exception if all retry fails.
        """
        self._conn_str = (
            f"host={host} port={port} dbname={dbname} user={user} password={password}"
        )
        self._conn_retry_limit = 20
        self._conn_retry_interval = 2
        self._active = False

        retry = 0
        for _ in range(self._conn_retry_limit):
            try:
                retry += 1
                self._conn = psycopg2.connect(self._conn_str)
            except Exception as e:
                logger.info(
                    f"PostgresGateway connection failed, will retry for #{retry} "
                    f"in {self._conn_retry_interval} seconds. Error: {e}"
                )
                sleep(self._conn_retry_interval)
                continue
            else:
                self._active = True
                break
        if not self._active:
            logger.error(
                f"PostgresGateway connection failed after {retry} times, stopping retry."
            )
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

    @staticmethod
    def _read_user_query(user_id: int = None, username: str = None):
        query = "SELECT user_id, username, nickname, password, salt, email, created_at FROM users WHERE "
        if user_id:
            return query + "user_id = %s", user_id
        elif username:
            return query + "username = %s", username
        else:
            return None, None

    def query(self, query: str, *args) -> Any:
        """Given a `query` string, do the query and return result.
        """
        try:
            cur = self._conn.cursor()
            cur.execute(query, args)
            result = (
                cur.fetchone()
                if not query.lstrip().upper().startswith(("UPDATE", "DELETE"))
                else cur.rowcount
            )
            self._conn.commit()
            cur.close()
            return result
        except (Exception, psycopg2.DatabaseError) as e:
            logger.error(f"PostgresGateway failed on query: '{query}' with {args}.")
            raise DatabaseQueryError(f"Query {query} with {args} failed: {e}")

    def create_user(self, user: User) -> int:
        """Given a `user` object, create user entry in database table and return
        an integer of `user_id` of created user. Returns -1 if creation fails.
        """
        query = """INSERT INTO users(username, nickname, email, password, salt, created_at)
                   VALUES (%s, %s, %s, %s, %s, %s) RETURNING user_id"""
        user_id = self.query(
            query,
            user.username,
            user.nickname,
            user.email,
            user.password,
            user.salt,
            user.created_at,
        )
        return user_id[0] if user_id and len(user_id) == 1 else -1

    def read_user(self, user_id: int = None, username: str = None) -> User:
        """Given a `user_id` integer, read user info from database and return a
        `User` object.
        """
        if user_id is not None and user_id <= 0:
            return User(valid=False)
        query, key = PostgresGateway._read_user_query(user_id, username)
        result = self.query(query, username) if query else None
        return (
            User(
                user_id=result[0],
                username=result[1],
                nickname=result[2],
                password=bytes(result[3]),
                salt=bytes(result[4]),
                email=result[5],
                created_at=result[6],
                valid=True,
            )
            if result is not None
            else User()
        )

    def update_user(self, user_id: int, **kwargs) -> bool:
        """Given a `user_id` integer and keyword only arguments, update fields
        specified in `kwargs`. Return a boolean indicating if update succeeds.
        """
        field_names, field_vals = generate_update_params(user_id, **kwargs)
        if user_id <= 0 or len(field_vals) == 0:
            return False
        query = f"""UPDATE users SET {field_names} WHERE user_id = %s"""
        result = self.query(query, *field_vals)
        return result == 1

    def delete_user(self, user_id: int) -> bool:
        """Given a `user_id` integer, delete user from database table and return a
        boolean indicating if the operation succeeds or not.
        """
        if user_id <= 0:
            return False
        query = """DELETE FROM users WHERE user_id = %s"""
        result = self.query(query, user_id)
        return result == 1


def make_postgres_gateway(filename="database.ini") -> PostgresGateway:
    """Factory method to create a `PostgresGateway` object.
    """
    try:
        config = read_postgres_config(filename)
        return PostgresGateway(
            host=config["host"],
            port=int(config["port"]),
            dbname=config["dbname"],
            user=config["user"],
            password=config["password"],
        )
    except KeyError as e:
        logger.error(f"Invalid database config file: {e}")
        raise e
    except Exception as e:
        logger.error(f"Failed to initialize PostgresGateway: {e}")
        raise e
