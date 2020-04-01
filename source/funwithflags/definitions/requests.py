"""Module for user signup request."""
from dataclasses import dataclass
import re
from typing import Mapping

from .exceptions import BadRequestError


password_reg = (
    r"""^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"""
)
email_reg = r"""^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"""

password_pat = re.compile(password_reg)
email_pat = re.compile(email_reg)


def validate_password(password: str) -> bool:
    """Check if a string is a valid password string. Returns true if valid.
    """
    return True if re.search(password_pat, password) else False


def validate_email(email: str) -> bool:
    """Check if an email address is valid. Returns true if valid.
    """
    return True if re.search(email_pat, email) else False


@dataclass
class RegisterRequest:
    username: str
    nickname: str
    email: str
    password: str

    def __post_init__(self):
        if (
            len(self.username) < 3
            or not validate_email(self.email)
            or not validate_password(self.password)
        ):
            raise BadRequestError("Invalid username, email or password")


@dataclass
class LoginRequest:
    username: str
    password: str


@dataclass
class LogoutRequest:
    jti:     str


@dataclass
class UserUpdateRequest:
    user_id: int
    fields: Mapping[str, str]
    protected: bool = False

    def __post_init__(self):
        self.fields = {field: value for field, value in self.fields.items() if UserUpdateRequest._is_valid_field(field)}
        if len(self.fields) == 0:
            raise BadRequestError("No valid fields")
        if self.protected:
            for field, value in self.fields.items():
                if field == "username" and len(value) < 3:
                    raise BadRequestError("Invalid username")
                if field == "email" and not validate_email(value):
                    raise BadRequestError("Invalid email")
                if field == "password" and not validate_password(value):
                    raise BadRequestError("Invalid password")
        else:
            for field, value in self.fields.items():
                if UserUpdateRequest._is_protected_field(field):
                    raise BadRequestError("No access to update protected field")

    _valid_fields = {"username", "nickname", "email", "password"}
    _protected_fields = {"username", "email", "password"}

    @staticmethod
    def _is_valid_field(name: str):
        return name in UserUpdateRequest._valid_fields

    @staticmethod
    def _is_protected_field(name: str):
        return name in UserUpdateRequest._protected_fields
