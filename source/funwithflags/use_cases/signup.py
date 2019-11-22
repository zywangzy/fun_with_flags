"""Module for user signup implementation."""
from funwithflags.definitions import SignupRequest, User
from funwithflags.entities import hash_password_and_salt
from funwithflags.gateways import Context


def signup(request: SignupRequest, context: Context):
    """Given a `SignupRequest` object and `Context` of gateways, execute signup logic.
    This will create a valid `User` object and write it into Postgres database table.
    Return user id got from db gateway.
    """
    hashed_password, salt = hash_password_and_salt(request.password)
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
