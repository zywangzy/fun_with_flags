"""Module for user login implementation."""

from flask_jwt_simple import create_jwt

from funwithflags.definitions import LoginRequest
from funwithflags.definitions import BadRequestError, DatabaseQueryError
from funwithflags.entities import hash_password_with_salt
from funwithflags.gateways import Context


def login(request: LoginRequest, context: Context) -> (str, str):
    user = context.postgres_gateway.read_user(username=request.username)
    if not user.valid:
        raise DatabaseQueryError
    hash_val = hash_password_with_salt(request.password, user.salt)
    if hash_val != user.password:
        raise BadRequestError
    # TODO: generate jwt
    jwt = create_jwt(identity=user.user_id)
    # TODO: Write jwt to Redis (need override?)
    return request.username, jwt
