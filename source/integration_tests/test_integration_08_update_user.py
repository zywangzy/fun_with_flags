"""Integration test for updating user."""
import bcrypt
import pytest

from funwithflags.definitions import UserUpdateRequest, BadRequestError, DatabaseQueryError
from funwithflags.use_cases import update_user

from .conftest import EXAMPLE_USER

global_user_id = 0


@pytest.fixture
def get_user_id(context):
    global global_user_id
    if global_user_id == 0:
        global_user_id = context.postgres_gateway.read_user(username=EXAMPLE_USER.username).user_id


@pytest.mark.parametrize(
    "user_id,kwargs,protected,exception",
    [(-1, {}, False, BadRequestError),
     (0, {}, False, BadRequestError),
     (1, {}, False, BadRequestError),
     (1, {"nickname": "abc"}, False, DatabaseQueryError),
     (1, {"username": "userName"}, True, DatabaseQueryError)]
)
def test_update_user_failure(context, user_id, kwargs, protected, exception):
    # When & Then
    with pytest.raises(exception):
        if user_id is None:
            global global_user_id
            user_id = global_user_id
        request = UserUpdateRequest(user_id=user_id, fields=kwargs, protected=protected)
        update_user(update_request=request, context=context)


@pytest.mark.parametrize(
    "fields,protected",
    [({"nickname": "abc"}, False),
     ({"username": "test1"}, True),
     ({"username": "newName", "password": "AbC123@"}, True)]
)
def test_update_user(monkeypatch, get_user_id, context, fields, protected):
    # Given
    global global_user_id
    user_id = global_user_id

    # Monkeypatch hashpw
    def mock_hashpw(password, salt):
        return b"abcdef123456"

    monkeypatch.setattr(bcrypt, "hashpw", mock_hashpw)

    # When & Then
    request = UserUpdateRequest(user_id=user_id, fields=fields, protected=protected)
    update_user(update_request=request, context=context)
