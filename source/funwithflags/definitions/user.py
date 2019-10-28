"""Module defining the User class."""
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    """Class representing a User.
    """

    user_id: int
    username: str
    nickname: str
    email: str
    password: bytearray
    salt: bytearray
    created_at: datetime
