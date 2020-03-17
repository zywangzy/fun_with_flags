"""Module for user login implementation."""

import flask_jwt_extended

from funwithflags.definitions import LoginRequest
from funwithflags.definitions import BadRequestError, DatabaseQueryError
from funwithflags.entities import hash_password_with_salt
from funwithflags.gateways import Context


def login(request: LoginRequest, context: Context) -> (str, str, str):
    """Given user login request, check if provided username and password are valid. If yes, provide a tuple consisting
    username, access token and refresh token. If username doesn't exist, raise `DatabaseQueryError`; if username is
    valid but password doesn't match, raise `BadRequestError`.
    """
    user = context.postgres_gateway.read_user(username=request.username)
    if not user.valid:
        raise DatabaseQueryError
    hash_val = hash_password_with_salt(request.password, user.salt)
    if hash_val != user.password:
        raise BadRequestError
    access_token = flask_jwt_extended.create_access_token(identity=user.user_id, fresh=True)
    refresh_token = flask_jwt_extended.create_refresh_token(identity=user.user_id)
    context.redis_gateway.put(flask_jwt_extended.get_jti(encoded_token=access_token), "login")
    context.redis_gateway.put(flask_jwt_extended.get_jti(encoded_token=refresh_token), "login")
    return request.username, access_token, refresh_token
