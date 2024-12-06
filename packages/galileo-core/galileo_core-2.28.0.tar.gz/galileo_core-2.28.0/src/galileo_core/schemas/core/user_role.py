from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    user = "user"
    read_only = "read_only"
