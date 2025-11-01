from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"


class OrderEnum(str, Enum):
    ASC = "asc"
    DESC = "desc"