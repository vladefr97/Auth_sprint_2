import string
from secrets import choice as secrets_choice

from core.models import DefaultUserRole
from db.models import User
from db.models.social_account import SocialAccount
from db.models.userrole import UserRole


def generate_random_string():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets_choice(alphabet) for _ in range(16))


def register_user_if_not_exists(email: str,
                                login: str) -> User:
    current_user = User.find_by_email(email=email)
    if not current_user:
        current_user = User.find_by_login(login=login)

    if not current_user:
        role_name = DefaultUserRole.USER.value
        role_model = UserRole.get_role(user_role_type=role_name)
        current_user = User(login=login, email=email, password=User.generate_hash(generate_random_string()),
                            user_role=role_model.id)
        current_user.save_to_db()

    return current_user


def attach_social_account_to_user(social_name: str,
                                  social_id: str, user: User):
    if not SocialAccount.exists(
            user_id=user.id, social_id=social_id, social_name=social_name
    ):
        SocialAccount(
            user_id=user.id, social_id=social_id, social_name=social_name
        ).save_to_db()