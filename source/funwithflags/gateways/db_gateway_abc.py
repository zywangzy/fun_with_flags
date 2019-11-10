"""Module for the DbGateway abstract base class."""
from abc import ABC, abstractmethod
from typing import List

from funwithflags.definitions.user import User


class DbGateway(ABC):
    """Abstract base class for DbGateway defining the interfaces to interact with
    a database, including read / write / update / delete database table entries.
    """

    @abstractmethod
    def query(self, command: str) -> List:
        """Given a `command` string, do the query and return a list of results.
        """

    @abstractmethod
    def create_user(self, user: User) -> int:
        """Given a `user` object, create user entry in database table and return
        an integer of `user_id` of created user.
        """

    @abstractmethod
    def read_user(self, user_id: int) -> User:
        """Given a `user_id` integer, read user info from database and return a
        `User` object.
        """
