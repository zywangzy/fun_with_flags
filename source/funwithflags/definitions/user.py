"""Module defining the User class."""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    """Class representing a User.
    """

    user_id: int = -1
    username: str = ""
    nickname: str = ""
    email: str = ""
    password: bytes = b""
    salt: bytes = b""
    created_at: datetime = datetime.now()
    valid: bool = False
