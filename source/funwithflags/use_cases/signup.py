"""Module for user signup implementation."""
from funwithflags.definitions import SignupRequest, User
from funwithflags.entities import generate_salt, hash_password
from funwithflags.gateways import Context


def signup(request: SignupRequest, context: Context):
    """Given a `SignupRequest` object and `Context` of gateways, execute signup logic.
    This will create a valid `User` object and write it into Postgres database table.
    Return user id got from db gateway.
    """
    salt: bytearray = generate_salt()
    hashed_password: bytearray = hash_password(request.password, salt)
    user = User(
        username=request.username,
        nickname=request.nickname,
        email=request.email,
        password=hashed_password,
        salt=salt,
        valid=True,
    )
    user_id = context.postgres_gateway.create_user(user)
    return user_id
