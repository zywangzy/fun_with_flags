"""Module for refreshing access token implementation"""
from typing import Any

import flask_jwt_extended

from funwithflags.gateways.context import Context


def refresh_access_token(identity: Any, context: Context) -> str:
    """Give refresh token, refresh the user (identity is user_id) login status and return a new access token.
    """
    new_token = flask_jwt_extended.create_access_token(identity=identity)
    context.redis_gateway.set(flask_jwt_extended.get_jti(encoded_token=new_token), "login")
    return new_token
