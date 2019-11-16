"""Module for user signup request."""
from dataclasses import dataclass


@dataclass
class SignupRequest:
    username: str
    nickname: str
    email: str
    password: str
