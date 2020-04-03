"""Module for user fresh login implementation."""

import flask_jwt_extended

from funwithflags.definitions import RefreshLoginRequest
from funwithflags.definitions import BadRequestError
from funwithflags.definitions import ACCESS_EXPIRES
from funwithflags.entities import hash_password_with_salt
from funwithflags.gateways import Context


def fresh_login(request: RefreshLoginRequest, context: Context) -> str:
    """Given user refresh login request, check if provided user id and password are valid. If yes, provide an access
    token string. If user id doesn't exist, raise `DatabaseQueryError`; if username is valid but password doesn't match,
    raise `BadRequestError`.
    """
    user = context.postgres_gateway.read_user(user_id=request.user_id)
    hash_val = hash_password_with_salt(request.password, user.salt)
    if hash_val != user.password:
        raise BadRequestError
    access_token = flask_jwt_extended.create_access_token(identity=user.user_id, fresh=True)
    context.redis_gateway.set(flask_jwt_extended.get_jti(encoded_token=access_token), "login", ACCESS_EXPIRES * 1.2)
    return access_token
