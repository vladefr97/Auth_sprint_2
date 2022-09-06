from core.models import DefaultUserRole
from db.connection import get_db_instance
from db.models.userrole import UserRole


def create_default_user_roles() -> None:
    db_instance = get_db_instance()
    for default_role in DefaultUserRole:
        if not UserRole.get_role(default_role.value):
            new_role = UserRole(role_type=default_role.value)
            db_instance.session.add(new_role)
            db_instance.session.commit()
