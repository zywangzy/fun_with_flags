"""Module for user authentication/authorization api."""
from typing import Any, Mapping

import flask_jwt_extended

from funwithflags.definitions import User
from funwithflags.definitions import RegisterRequest, LoginRequest, FreshLoginRequest, LogoutRequest, UserUpdateRequest
from funwithflags.definitions import BadRequestError, DatabaseQueryError
from funwithflags.definitions import ACCESS_EXPIRES, REFRESH_EXPIRES
from funwithflags.entities import generate_salt_hash_password, hash_password_with_salt
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


def login(request: LoginRequest, context: Context) -> (str, str, str):
    """Given user login request, check if provided username and password are valid. If yes, provide a tuple consisting
    username, access token and refresh token. If username doesn't exist, raise `DatabaseQueryError`; if username is
    valid but password doesn't match, raise `BadRequestError`.
    """
    user = context.postgres_gateway.read_user(username=request.username)
    if hash_password_with_salt(request.password, user.salt) != user.password:
        raise BadRequestError
    access_token = flask_jwt_extended.create_access_token(identity=user.user_id, fresh=True)
    refresh_token = flask_jwt_extended.create_refresh_token(identity=user.user_id)
    context.redis_gateway.set(flask_jwt_extended.get_jti(encoded_token=access_token), "login", ACCESS_EXPIRES * 1.2)
    context.redis_gateway.set(flask_jwt_extended.get_jti(encoded_token=refresh_token), "login", REFRESH_EXPIRES * 1.2)
    return request.username, access_token, refresh_token


def fresh_login(request: FreshLoginRequest, context: Context) -> str:
    """Given user refresh login request, check if provided user id and password are valid. If yes, provide an access
    token string. If user id doesn't exist, raise `DatabaseQueryError`; if username is valid but password doesn't match,
    raise `BadRequestError`.
    """
    user = context.postgres_gateway.read_user(user_id=request.user_id)
    if hash_password_with_salt(request.password, user.salt) != user.password:
        raise BadRequestError
    access_token = flask_jwt_extended.create_access_token(identity=user.user_id, fresh=True)
    context.redis_gateway.set(flask_jwt_extended.get_jti(encoded_token=access_token), "login", ACCESS_EXPIRES * 1.2)
    return access_token


def refresh_access_token(identity: Any, context: Context) -> str:
    """Give refresh token, refresh the user (identity is user_id) login status and return a new access token.
    """
    new_token = flask_jwt_extended.create_access_token(identity=identity)
    context.redis_gateway.set(flask_jwt_extended.get_jti(encoded_token=new_token), "login")
    return new_token


def logout(logout_request: LogoutRequest, context: Context):
    """Logout user with given logout request and context. Current logic is trying to be simple and doesn't check if
    the refresh token is already logged out in Redis cache.
    """
    context.redis_gateway.set(logout_request.jti, "logout", REFRESH_EXPIRES * 1.2)


def read_user_basic(user_id: int, context: Context) -> Mapping[str, Any]:
    """Read basic user info. Return a map of field names and values."""
    user = context.postgres_gateway.read_user(user_id=user_id)
    return {
        "userid": user.user_id,
        "username": user.username,
        "nickname": user.nickname,
        "email": user.email,
        "created_at": str(user.created_at)
    }


def read_user_details(user_id: int, context: Context) -> Mapping[str, Any]:
    """Read user info details. Return a map of field names and values.
    """
    #  TODO: implement reading user details
    return read_user_basic(user_id, context)


def update_user(update_request: UserUpdateRequest, context: Context) -> None:
    """Update user info. Return a None object if update succeeds, otherwise throw exceptions.
    """
    password = update_request.fields.get("password", None)
    if password is not None:
        user = context.postgres_gateway.read_user(user_id=update_request.user_id)
        update_request.fields["password"] = hash_password_with_salt(password, user.salt)
    context.postgres_gateway.update_user(user_id=update_request.user_id, **update_request.fields)
