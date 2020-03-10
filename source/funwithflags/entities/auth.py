"""Module for authentication utilities."""
import bcrypt


def hash_password_with_salt(password: str, salt: bytes) -> bytes:
    """Hash a password string with a salt bytes."""
    return bcrypt.hashpw(bytes(password.encode()), salt)


def generate_salt_hash_password(password: str) -> (bytes, bytes):
    """Hash a password string with generated salt, return a 'bytes' hashed password and the 'bytes' salt."""
    salt = bcrypt.gensalt()
    return hash_password_with_salt(password, salt), salt
