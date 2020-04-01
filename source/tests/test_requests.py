"""Module to test requests."""
import pytest

from funwithflags.definitions import (
    BadRequestError,
    RegisterRequest,
    UserUpdateRequest,
    validate_email,
    validate_password,
)


@pytest.mark.parametrize(
    "password,expected",
    [
        ("", False),
        ("a", False),
        ("abc123", False),
        ("AbC123@", True),
        ("123456", False),
        ("AbCdEfGhIjKl12345678$", False),
    ],
)
def test_validate_password(password, expected):
    # When
    result = validate_password(password)
    # Then
    assert expected == result


@pytest.mark.parametrize(
    "email,expected",
    [
        ("", False),
        ("a", False),
        ("prefix@", False),
        ("prefix@domain", False),
        ("prefix@domain.com", True),
    ],
)
def test_validate_email(email, expected):
    # When
    result = validate_email(email)
    # Then
    assert expected == result


@pytest.mark.parametrize(
    "kwargs",
    [
        {"username": "", "nickname": "", "email": "", "password": ""},
        {
            "username": "a",
            "nickname": "",
            "email": "test@example.com",
            "password": "aValidPassword1#",
        },
        {
            "username": "abc",
            "nickname": "",
            "email": "test@example",
            "password": "aValidPassword1#",
        },
        {
            "username": "user",
            "nickname": "",
            "email": "test@example.com",
            "password": "aValidPassword1",
        },
    ],
)
def test_signup_request_failure(kwargs):
    with pytest.raises(BadRequestError) as exc:
        # When
        _ = RegisterRequest(**kwargs)
    # Then
    assert "Invalid username, email or password" in str(exc)


@pytest.mark.parametrize(
    "user_id,fields,protected,exception,message",
    [(1, {}, False, BadRequestError, "No valid fields"),
     (2, {"invalid_field": "value"}, False, BadRequestError, "No valid fields"),
     (3, {"username": "justAName"}, False, BadRequestError, "No access to update protected field"),
     (4, {"username": "a"}, True, BadRequestError, "Invalid username"),
     (5, {"password": "invalid"}, True, BadRequestError, "Invalid password"),
     (6, {"email": "invalidEmail"}, True, BadRequestError, "Invalid email")]
)
def test_update_user_request_failure(user_id, fields, protected, exception, message):
    with pytest.raises(exception) as exc:
        # When
        _ = UserUpdateRequest(user_id=user_id, fields=fields, protected=protected)
    # Then
    assert message in str(exc)
