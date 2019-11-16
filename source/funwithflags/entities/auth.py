"""Module for authentication utilities."""
import bcrypt


def generate_salt() -> bytearray:
    return bcrypt.gensalt()


def hash_password(password, salt) -> bytearray:
    return bcrypt.hashpw(password, salt)
