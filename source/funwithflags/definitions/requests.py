"""Module for user signup request."""
from dataclasses import dataclass
import re

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
class SignupRequest:
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
