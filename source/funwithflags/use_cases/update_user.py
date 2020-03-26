"""Module for updating user."""
from funwithflags.definitions import UserUpdateRequest, BadRequestError, DatabaseQueryError
from funwithflags.entities import hash_password_with_salt
from funwithflags.gateways import Context


def update_user(update_request: UserUpdateRequest, context: Context):
    password = update_request.fields.get("password", None)
    if password is not None:
        user = context.postgres_gateway.read_user(user_id=update_request.user_id)
        if not user.valid:
            raise DatabaseQueryError
        update_request.fields["password"] = hash_password_with_salt(password, user.salt)
    if not context.postgres_gateway.update_user(user_id=update_request.user_id, **update_request.fields):
        raise BadRequestError("Unable to update")
