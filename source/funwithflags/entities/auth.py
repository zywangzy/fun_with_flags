"""Module for authentication utilities."""
import bcrypt


def hash_password_and_salt(password: str) -> (bytes, bytes):
    """Hash a password string with generated salt, return a 'bytes' hashed password and the 'bytes' salt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes(password.encode()), salt), salt
