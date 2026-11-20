
import os
import time
import jwt

secret = os.getenv("JWT_SECRET")

if not secret:
    raise RuntimeError("JWT_SECRET is not configured.")

now = int(time.time())

payload = {
    "sub": "employee001",
    "role": "admin",
    "iss": "centralised-api-authorisation",
    "aud": "api-services",
    "iat": now,
    "exp": now + 3600
}

token = jwt.encode(
    payload,
    secret,
    algorithm="HS256"
)

print("\nEmployee JWT token:\n")
print(token)
