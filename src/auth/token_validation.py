

import os
import jwt

from jwt import InvalidTokenError


JWT_SECRET = os.getenv("JWT_SECRET")

JWT_ALGORITHM = "HS256"
JWT_ISSUER = "centralised-api-authorisation"
JWT_AUDIENCE = "api-services"


def validate_token(token: str) -> dict:
    """
    Validate a JWT and return its trusted claims.
    """

    if not JWT_SECRET:
        raise RuntimeError(
            "JWT_SECRET environment variable is not configured."
        )

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            issuer=JWT_ISSUER,
            audience=JWT_AUDIENCE,
            options={
                "require": ["exp", "iat", "iss", "aud", "sub"]
            }
        )

        return payload

    except InvalidTokenError as error:
        raise ValueError("Token validation failed.") from error
