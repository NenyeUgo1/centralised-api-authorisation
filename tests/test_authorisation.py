
import pytest

from src.auth.authorisation import has_permission
from src.auth.roles import Role
from src.auth.permissions import Permission


def test_employee_can_read_own_records():
    assert has_permission(
        Role.EMPLOYEE,
        Permission.EMPLOYEE_READ_OWN
    ) is True


def test_employee_cannot_read_finance_records():
    assert has_permission(
        Role.EMPLOYEE,
        Permission.FINANCE_READ
    ) is False


def test_manager_can_read_team_records():
    assert has_permission(
        Role.MANAGER,
        Permission.EMPLOYEE_READ_TEAM
    ) is True


def test_finance_can_update_finance_records():
    assert has_permission(
        Role.FINANCE,
        Permission.FINANCE_UPDATE
    ) is True


def test_finance_cannot_manage_employees():
    assert has_permission(
        Role.FINANCE,
        Permission.EMPLOYEE_MANAGE
    ) is False


def test_admin_has_all_permissions():
    for permission in Permission:
        assert has_permission(Role.ADMIN, permission) is True


def test_unknown_role_is_denied():
    assert has_permission(
        "unknown",
        Permission.FINANCE_READ
    ) is False


def test_unknown_permission_is_denied():
    assert has_permission(
        Role.EMPLOYEE,
        "unknown:permission"
    ) is False
