
import os
import time
import jwt
import pytest

# Development-only secret. Never use this in production.
TEST_SECRET = "local-development-secret-at-least-32-characters"

# Set the secret before importing the validation module.
os.environ["JWT_SECRET"] = TEST_SECRET

from src.auth.token_validation import validate_token


def create_test_token(expiration):
    now = int(time.time())

    payload = {
        "sub": "user123",
        "role": "employee",
        "iss": "centralised-api-authorisation",
        "aud": "api-services",
        "iat": now,
        "exp": expiration
    }

    return jwt.encode(
        payload,
        TEST_SECRET,
        algorithm="HS256"
    )


# TEST 1: A valid token should be accepted.
def test_valid_token():
    token = create_test_token(int(time.time()) + 300)

    claims = validate_token(token)

    assert claims["sub"] == "user123"
    assert claims["role"] == "employee"


# TEST 2: An expired token should be rejected.
def test_expired_token():
    token = create_test_token(int(time.time()) - 60)

    with pytest.raises(ValueError):
        validate_token(token)


# TEST 3: A token with an invalid signature should be rejected.
def test_invalid_signature():
    token = create_test_token(int(time.time()) + 300)

    tampered_token = token[:-5] + "abcde"

    with pytest.raises(ValueError):
        validate_token(tampered_token)
