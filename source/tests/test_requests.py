"""Module to test requests."""
import pytest

from funwithflags.definitions import (
    BadRequestError,
    SignupRequest,
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
        _ = SignupRequest(**kwargs)
    # Then
    assert "Invalid username, email or password" in str(exc)
