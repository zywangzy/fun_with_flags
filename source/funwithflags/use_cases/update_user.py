"""Module for updating user."""
from funwithflags.definitions import UserUpdateRequest, BadRequestError
from funwithflags.gateways import Context


def update_user(update_request: UserUpdateRequest, context: Context):
    if not context.postgres_gateway.update_user(user_id=update_request.user_id, **update_request.fields):
        raise BadRequestError("Unable to update")
