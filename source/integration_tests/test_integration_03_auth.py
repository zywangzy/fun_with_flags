"""Integration tests for auth apis."""
import pytest

import bcrypt
import flask_jwt_extended

from funwithflags.definitions import RegisterRequest, LoginRequest, FreshLoginRequest, LogoutRequest, UserUpdateRequest
from funwithflags.definitions import BadRequestError, DatabaseQueryError
from funwithflags.use_cases import register, login, fresh_login, refresh_access_token, logout, read_user_basic, update_user

from .conftest import CREATE_TIME, LOGIN_USER

LOGIN_USER_ID = -1


"""Tests for register"""


@pytest.mark.usefixtures("context")
def test_register(context):
    # Given
    request = RegisterRequest(
        username=LOGIN_USER.username,
        nickname=LOGIN_USER.nickname,
        email=LOGIN_USER.email,
        password=LOGIN_USER.password,
    )
    # When
    result = register(request, context)
    # Then
    assert isinstance(result, int)
    assert result > 0
    # Set global variable for further tests
    global LOGIN_USER_ID
    LOGIN_USER_ID = result


"""Tests for login"""


@pytest.mark.usefixtures("context")
def test_login(monkeypatch, context):
    # Given
    expected_username = LOGIN_USER.username
    request = LoginRequest(
        username=expected_username,
        password="Password123@"
    )
    expected_access_token = "expected.Access.Token"
    expected_refresh_token = "expected.Refresh.Token"
    expected_access_jti = "expected.Access.Jti"
    expected_refresh_jti = "expected.Refresh.Jti"

    # Monkeypatch flask_jwt_extended
    def mock_create_access_token(identity, fresh):
        return expected_access_token

    def mock_create_refresh_token(identity):
        return expected_refresh_token

    def mock_get_jti(encoded_token):
        if encoded_token == expected_access_token:
            return expected_access_jti
        elif encoded_token == expected_refresh_token:
            return expected_refresh_jti

    monkeypatch.setattr(flask_jwt_extended, 'create_access_token', mock_create_access_token)
    monkeypatch.setattr(flask_jwt_extended, 'create_refresh_token', mock_create_refresh_token)
    monkeypatch.setattr(flask_jwt_extended, 'get_jti', mock_get_jti)

    # When
    username, access_token, refresh_token = login(request, context)
    cache_access_value = context.redis_gateway.get(expected_access_jti)
    cache_refresh_value = context.redis_gateway.get(expected_refresh_jti)

    # Then
    assert username == expected_username
    assert access_token == expected_access_token
    assert refresh_token == expected_refresh_token
    assert cache_access_value and cache_access_value == "login"
    assert cache_refresh_value and cache_refresh_value == "login"


@pytest.mark.usefixtures("context")
def test_login_user_not_found_failure(context):
    # Given
    request = LoginRequest(
        username="noSuchUser",  # Non-existent
        password="password"
    )
    # When & Then
    with pytest.raises(DatabaseQueryError):
        login(request, context)


@pytest.mark.usefixtures("context")
def test_login_wrong_password_failure(context):
    # Given
    request = LoginRequest(
        username=LOGIN_USER.username,
        password="wrongPassword"
    )
    # When & Then
    with pytest.raises(BadRequestError):
        login(request, context)


@pytest.mark.usefixtures("context")
def test_login_user_not_found_failure(context):
    # Given
    request = FreshLoginRequest(
        user_id=1000,  # Non-existent
        password="password"
    )
    # When & Then
    with pytest.raises(DatabaseQueryError):
        fresh_login(request, context)


@pytest.mark.usefixtures("context")
def test_login_wrong_password_failure(context):
    # Given
    request = FreshLoginRequest(
        user_id=LOGIN_USER_ID,
        password="wrongPassword"
    )
    # When & Then
    with pytest.raises(BadRequestError):
        fresh_login(request, context)


"""Tests for fresh login"""


@pytest.mark.usefixtures("context")
def test_fresh_login(monkeypatch, context):
    # Given
    request = FreshLoginRequest(
        user_id=LOGIN_USER_ID,
        password="Password123@"
    )
    expected_access_token = "expected.Access.Token"
    expected_access_jti = "expected.Access.Jti"

    # Monkeypatch flask_jwt_extended
    def mock_create_access_token(identity, fresh):
        return expected_access_token

    def mock_get_jti(encoded_token):
        return expected_access_jti

    monkeypatch.setattr(flask_jwt_extended, 'create_access_token', mock_create_access_token)
    monkeypatch.setattr(flask_jwt_extended, 'get_jti', mock_get_jti)

    # When
    access_token = fresh_login(request, context)
    cache_access_value = context.redis_gateway.get(expected_access_jti)

    # Then
    assert access_token == expected_access_token
    assert cache_access_value and cache_access_value == "login"


"""Tests for refresh access token"""


@pytest.mark.usefixtures("context")
def test_refresh_access_token(monkeypatch, context):
    # Given
    expected_access_token = "fake.Access.Token"
    expected_jti = "new.Token"
    expected_status = "login"

    # Monkeypatch flask_jwt_extended

    def mock_create_access_token(identity):
        return expected_access_token

    def mock_get_jti(encoded_token):
        return expected_jti

    monkeypatch.setattr(flask_jwt_extended, 'create_access_token', mock_create_access_token)
    monkeypatch.setattr(flask_jwt_extended, 'get_jti', mock_get_jti)

    # When
    new_token = refresh_access_token(identity=10, context=context)
    status = context.redis_gateway.get(expected_jti)

    # Then
    assert expected_access_token == new_token
    assert expected_status == status


"""Tests for logout"""


@pytest.mark.usefixtures("context")
def test_logout(context):
    # Given
    jti = "fake.jti"
    expected_status = "logout"

    # When
    logout(LogoutRequest(jti), context)

    # Then
    status = context.redis_gateway.get(jti)
    assert status and expected_status == status


"""Tests for read user"""


def test_read_user_basic(context):
    # Given
    expected_user_id = LOGIN_USER_ID
    # When
    result = read_user_basic(user_id=expected_user_id, context=context)
    # Then
    assert len(result) == 5
    assert result["userid"] == expected_user_id
    assert result["username"] == LOGIN_USER.username
    assert result["nickname"] == LOGIN_USER.nickname
    assert result["email"] == LOGIN_USER.email
    assert result["created_at"] == str(CREATE_TIME)


@pytest.mark.parametrize(
    "user_id,exception",
    [(-1, BadRequestError),
     (0, BadRequestError),
     (1, DatabaseQueryError)]
)
def test_read_user_basic_failure(context, user_id, exception):
    # When & Then
    with pytest.raises(exception):
        read_user_basic(user_id=user_id, context=context)


"""Tests for update user"""


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
        user_id = LOGIN_USER_ID
        request = UserUpdateRequest(user_id=user_id, fields=kwargs, protected=protected)
        update_user(update_request=request, context=context)


@pytest.mark.parametrize(
    "fields,protected",
    [({"nickname": "abc"}, False),
     ({"username": "test1"}, True),
     ({"username": "newName", "password": "AbC123@"}, True)]
)
def test_update_user(monkeypatch, context, fields, protected):
    # Given
    global LOGIN_USER_ID
    user_id = LOGIN_USER_ID

    # Monkeypatch hashpw
    def mock_hashpw(password, salt):
        return b"abcdef123456"

    monkeypatch.setattr(bcrypt, "hashpw", mock_hashpw)

    # When & Then
    request = UserUpdateRequest(user_id=user_id, fields=fields, protected=protected)
    update_user(update_request=request, context=context)
