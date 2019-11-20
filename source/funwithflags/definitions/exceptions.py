"""Module defining exceptions."""
from dataclasses import dataclass


class ApplicationError(Exception):
    """Base class to be inherited by all exceptions in this application."""


@dataclass
class DatabaseQueryError(ApplicationError):
    """Exception of database query error."""

    message: str
