"""Module defining exceptions."""
from dataclasses import dataclass


class ApplicationError(Exception):
    """Base class to be inherited by all exceptions in this application."""


class DatabaseQueryError(ApplicationError):
    """Exception of database query error."""


class BadRequestError(ApplicationError):
    """Exception of bad user request error."""


class InternalError(ApplicationError):
    """Exception of unexpected internal error."""
