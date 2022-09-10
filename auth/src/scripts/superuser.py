from core.config import config
from core.models import DefaultUserRole
from db.relational.models import User
from db.relational.models.userrole import UserRole


def create_superuser() -> None:
    superuser_login = config.superuser_login

    if not User.find_by_login(superuser_login):
        superuser_role_type = UserRole.get_role(DefaultUserRole.SUPERUSER.value)
        superuser_password = config.superuser_password
        superuser = User(
            login=superuser_login, password=User.generate_hash(superuser_password), user_role=superuser_role_type.id
        )
        superuser.save_to_db()
