"""Module for reading user."""
from typing import Any, Mapping

from funwithflags.gateways import Context


def read_user_basic(user_id: int, context: Context) -> Mapping[str, Any]:
    """Read basic user info."""
    user = context.postgres_gateway.read_user(user_id=user_id)
    return {
        "userid": user.user_id,
        "username": user.username,
        "nickname": user.nickname,
        "email": user.email,
        "created_at": user.created_at
    }


def read_user_details(user_id: int, context: Context) -> Mapping[str, Any]:
    """Read user info details."""
    #  TODO: implement reading user details
    return read_user_basic(user_id, context)
