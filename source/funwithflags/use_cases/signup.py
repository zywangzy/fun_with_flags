"""Module for user signup implementation."""
from funwithflags.definitions import (
    Context,
    SignupRequest,
    User
)


def signup(request: SignupRequest, context: Context):

    user = User(
        username=request.username,
        nickname=request.nickname,
        email=request.email,
        password=bytearray(b""),
        salt=bytearray(b""),
        valid=True
    )
    context.postgres_gateway.create_user()
