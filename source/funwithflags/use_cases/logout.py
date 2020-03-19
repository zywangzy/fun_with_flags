"""Module for user logout implementation."""
import flask_jwt_extended

from funwithflags.definitions import LogoutRequest
from funwithflags.gateways import Context


def logout(logout_request: LogoutRequest, context: Context):
    """Logout user with given logout request and context. Current logic is trying to be simple and doesn't check if
    the refresh token is already logged out in Redis cache.
    """
    context.redis_gateway.set(flask_jwt_extended.get_jti(encoded_token=logout_request.token), "logout")
