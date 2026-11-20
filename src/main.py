
import os

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.auth.token_validation import validate_token
from src.auth.authorisation import has_permission
from src.auth.permissions import Permission


app = FastAPI(
    title="Centralised API Authorisation",
    description="A reusable JWT authentication and RBAC authorisation service.",
    version="1.0.0"
)

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        return validate_token(token)
    except (ValueError, RuntimeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired authentication token"
        )


def require_permission(required_permission: Permission):
    def permission_checker(user: dict = Depends(get_current_user)):
        user_role = user.get("role")

        if not has_permission(user_role, required_permission):
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this resource"
            )

        return user

    return permission_checker


@app.get("/")
def home():
    return {"message": "Centralised API Authorisation is running"}


@app.get("/employee/profile")
def employee_profile(
    user: dict = Depends(
        require_permission(Permission.EMPLOYEE_READ_OWN)
    )
):
    return {
        "message": "Employee profile accessed successfully",
        "user": user["sub"]
    }


@app.get("/finance/reports")
def finance_reports(
    user: dict = Depends(
        require_permission(Permission.FINANCE_READ)
    )
):
    return {
        "message": "Finance reports accessed successfully",
        "user": user["sub"]
    }


@app.get("/admin/users")
def admin_users(
    user: dict = Depends(
        require_permission(Permission.ADMIN_MANAGE)
    )
):
    return {
        "message": "Admin access granted",
        "user": user["sub"]
    }