import enum


class DefaultUserRole(enum.Enum):
    USER = "user"
    CONTENT_MANAGER = "content_manager"
    ADMIN = "admin"
    SUPERUSER = "superuser"
