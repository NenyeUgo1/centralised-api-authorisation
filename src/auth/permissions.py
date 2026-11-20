
from enum import Enum


class Permission(str, Enum):
    EMPLOYEE_READ_OWN = "employee:read:own"
    EMPLOYEE_READ_TEAM = "employee:read:team"
    EMPLOYEE_MANAGE = "employee:manage"

    FINANCE_READ = "finance:read"
    FINANCE_UPDATE = "finance:update"

    ADMIN_MANAGE = "admin:manage"
