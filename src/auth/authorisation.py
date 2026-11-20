
from src.auth.roles import Role
from src.auth.permissions import Permission


ROLE_PERMISSIONS = {
    Role.EMPLOYEE: {
        Permission.EMPLOYEE_READ_OWN,
    },

    Role.MANAGER: {
        Permission.EMPLOYEE_READ_OWN,
        Permission.EMPLOYEE_READ_TEAM,
        Permission.FINANCE_READ,
    },

    Role.FINANCE: {
        Permission.FINANCE_READ,
        Permission.FINANCE_UPDATE,
    },

    Role.ADMIN: set(Permission),
}


def has_permission(role: str | Role, permission: str | Permission) -> bool:
    """
    Check whether a role has the required permission.
    Access is denied by default.
    """

    try:
        user_role = Role(role)
        required_permission = Permission(permission)
    except ValueError:
        return False

    allowed_permissions = ROLE_PERMISSIONS.get(user_role, set())

    return required_permission in allowed_permissions