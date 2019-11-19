"""Module for authentication utilities."""
import bcrypt


def generate_salt() -> bytearray:
    """Generate a random salt and convert it from type 'bytes' to 'bytearray'."""
    return bytearray(bcrypt.gensalt())


def hash_password(password: str, salt: bytearray) -> bytearray:
    """Hash a password string with salt, return a 'bytearray' hashed password."""
    return bcrypt.hashpw(bytes(password.encode()), bytes(salt))
