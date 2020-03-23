"""Module for user logout implementation."""
import flask_jwt_extended

from funwithflags.definitions import LogoutRequest, REFRESH_EXPIRES
from funwithflags.gateways import Context


def logout(logout_request: LogoutRequest, context: Context):
    """Logout user with given logout request and context. Current logic is trying to be simple and doesn't check if
    the refresh token is already logged out in Redis cache.
    """
    context.redis_gateway.set(logout_request.jti, "logout", REFRESH_EXPIRES * 1.2)
