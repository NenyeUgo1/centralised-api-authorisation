
import os
import time
import jwt

# Use a dedicated secret for automated tests only.
TEST_SECRET = "local-development-secret-at-least-32-characters"
os.environ["JWT_SECRET"] = TEST_SECRET

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)



# Test-only secret. Never use this in production.
TEST_SECRET = "local-development-secret-at-least-32-characters"

client = TestClient(app)


def create_token(role):
    now = int(time.time())

    payload = {
        "sub": "test-user",
        "role": role,
        "iss": "centralised-api-authorisation",
        "aud": "api-services",
        "iat": now,
        "exp": now + 300
    }

    return jwt.encode(
        payload,
        TEST_SECRET,
        algorithm="HS256"
    )


def test_missing_token_is_rejected():
    response = client.get("/employee/profile")

    assert response.status_code in (401, 403)


def test_employee_can_access_profile():
    token = create_token("employee")

    response = client.get(
        "/employee/profile",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_employee_cannot_access_finance():
    token = create_token("employee")

    response = client.get(
        "/finance/reports",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403


def test_admin_can_access_employee_profile():
    token = create_token("admin")

    response = client.get(
        "/employee/profile",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_admin_can_access_finance_reports():
    token = create_token("admin")

    response = client.get(
        "/finance/reports",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_admin_can_access_admin_users():
    token = create_token("admin")

    response = client.get(
        "/admin/users",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
