
from enum import Enum


class Role(str, Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    FINANCE = "finance"
    ADMIN = "admin"
