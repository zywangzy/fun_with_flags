"""Module for user signup implementation."""
from funwithflags.definitions import RegisterRequest, User
from funwithflags.entities import generate_salt_hash_password
from funwithflags.gateways import Context


def register(request: RegisterRequest, context: Context):
    """Given a `RegisterRequest` object and `Context` of gateways, execute signup logic.
    This will create a valid `User` object and write it into Postgres database table.
    Return user id got from db gateway.
    """
    hashed_password, salt = generate_salt_hash_password(request.password)
    user = User(
        username=request.username,
        nickname=request.nickname,
        email=request.email,
        password=hashed_password,
        salt=salt,
        valid=True,
    )
    return context.postgres_gateway.create_user(user)
