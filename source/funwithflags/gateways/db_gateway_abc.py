"""Module for the DbGateway abstract base class."""
from abc import ABC, abstractmethod
from typing import Any


class DbGateway(ABC):
    """Abstract base class for DbGateway defining the interfaces to interact with
    a database, including read / write / update / delete database table entries.
    """

    @abstractmethod
    def query(self, command: str) -> Any:
        """Given a `command` string, do the query and return result of type `Any`.
        """
