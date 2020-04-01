"""Module for the Postgres database gateway."""
import logging
from time import sleep
from typing import Any, Optional

import psycopg2

from .db_gateway_abc import DbGateway
from funwithflags.definitions import BadRequestError, DatabaseQueryError, InternalError, User
from funwithflags.entities import generate_update_params, read_config_file


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
    def _read_user_query(user_id: Optional[int] = None, username: Optional[str] = None):
        """Given `user_id` integer and `username` string, generate pair of query
        string and user id or username to read the user. If `user_id` is not None,
        return query for reading by user id; else if `username` is not None, return
        query for reading by `username`; else return a pair of None.
        """
        query = "SELECT user_id, username, nickname, password, salt, email, created_at FROM users WHERE "
        if user_id:
            return query + "user_id = %s", user_id
        elif username:
            return query + "username = %s", username
        else:
            return None, None

    def query(self, query: str, *args) -> Any:
        """Given a `query` string, do the query and return result, raise a BadRequestError
        if query is invalid or DatabaseQueryError if anything wrong happens during query.
        """
        if query is None or len(query) == 0:
            raise BadRequestError("Invalid query statement")
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
        an integer of `user_id` of created user. Raise DatabaseQueryError if creation
        failed.
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
        if user_id and len(user_id) == 1:
            return user_id[0]
        else:
            raise DatabaseQueryError

    def read_user(self, user_id: Optional[int] = None, username: Optional[str] = None) -> User:
        """Given a `user_id` integer or a `username` string, read user info from
        database and return a `User` object. Raise BadRequestError if query argument
        is invalid or DatabaseQueryError if query failed.
        """
        if user_id is not None and user_id <= 0:
            raise BadRequestError("Invalid user id")
        query, key = PostgresGateway._read_user_query(user_id, username)
        try:
            result = self.query(query, key)
            return User(
                user_id=result[0],
                username=result[1],
                nickname=result[2],
                password=bytes(result[3]),
                salt=bytes(result[4]),
                email=result[5],
                created_at=result[6],
                valid=True,
            )
        except BadRequestError:
            raise BadRequestError("Invalid user id and username")
        except (Exception, DatabaseQueryError) as e:
            raise DatabaseQueryError

    def update_user(self, user_id: int, **kwargs) -> None:
        """Given a `user_id` integer and keyword only arguments, update fields
        specified in `kwargs`. Raise BadRequestError if update request is invalid
        or DatabaseQueryError if update query failed.
        """
        field_names, field_vals = generate_update_params(user_id, **kwargs)
        if user_id <= 0 or len(field_vals) == 0:
            raise BadRequestError("Invalid user id or update fields")
        query = f"""UPDATE users SET {field_names} WHERE user_id = %s"""
        result = self.query(query, *field_vals)
        if result != 1:
            raise DatabaseQueryError("Failed to update")

    def delete_user(self, user_id: int) -> None:
        """Given a `user_id` integer, delete user from database table and raise
        BadRequestError if user id is invalid or DatabaseQueryError if query
        failed.
        """
        if user_id <= 0:
            raise BadRequestError("Invalid user id")
        query = """DELETE FROM users WHERE user_id = %s"""
        result = self.query(query, user_id)
        if result != 1:
            raise DatabaseQueryError("Failed to delete")

    @staticmethod
    def create(filename="config.ini") -> DbGateway:
        """Factory method to create a `PostgresGateway` object.
        """
        try:
            section = "postgresql"
            config = read_config_file(filename, section)
            return PostgresGateway(
                host=config["host"],
                port=int(config["port"]),
                dbname=config["dbname"],
                user=config["user"],
                password=config["password"],
            )
        except KeyError as e:
            logger.error(f"Invalid config file \"{filename}\" section \"{section}\": {e}")
            raise e
        except Exception as e:
            logger.error(f"Failed to initialize PostgresGateway: {e}")
            raise e
