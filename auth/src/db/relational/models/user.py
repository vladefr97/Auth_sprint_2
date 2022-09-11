import string
from secrets import choice as secrets_choice

from core.models import DefaultUserRole
from db.relational.connection import db
from db.relational.models.mixins import TimeStampedMixin, UUIDMixin

# TODO: вынести в отдельный файл
from db.relational.models.userrole import UserRole
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.dialects.postgresql import UUID

EMAIL_MAX_LENGTH: int = 64


def generate_random_string() -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets_choice(alphabet) for _ in range(16))


class User(db.Model, UUIDMixin, TimeStampedMixin):
    # TODO: вынести названия таблиц и схем в константы
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True, "schema": "auth"}

    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    # TODO: заменить строковые названия таблицы
    user_role = db.Column(UUID(as_uuid=True), db.ForeignKey("auth.role.id", ondelete="cascade"))
    email = db.Column(db.String(length=EMAIL_MAX_LENGTH), nullable=False, unique=True)

    def __init__(self, **kwargs: str):
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f"<User {self.login}>"

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def save_user_with_default_role(cls, login: str, email: str, password: str) -> str:
        role_model = UserRole.get_role(user_role_type=DefaultUserRole.USER.value)
        user = User(email=email, login=login, password=password, user_role=role_model.id)
        user.save_to_db()
        return user

    @property
    def identity(self) -> str:
        """
        *Required Attribute or Property*
        flask-praetorian requires that the user class has an ``identity`` instance
        attribute or property that provides the unique id of the user instance
        """
        return str(self.id)

    @classmethod
    def get_random_user_password(self) -> str:
        return User.generate_hash(generate_random_string())

    @classmethod
    def find_by_login_or_email(cls, email: str, login: str) -> str:
        user = cls.find_by_login(login=login)
        if user:
            return user

        user = cls.find_by_email(email=email)
        if user:
            return user
        # TODO: вернуть ошибку?
        return None

    @classmethod
    def find_by_login(cls, login: str) -> str:
        return cls.query.filter_by(login=login).first()

    @classmethod
    def find_by_email(cls, email: str) -> str:
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, user_id: str) -> str:
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def return_all(cls) -> dict[str, list[dict[str, str]]]:
        def to_json(user: User) -> dict[str, str]:
            return {"login": user.login, "password": user.password}

        return {"users": [to_json(x) for x in User.query.all()]}

    @classmethod
    def delete_all(cls) -> dict[str, str]:
        # TODO: добавить try, except
        num_rows_deleted = db.session.query(cls).delete()
        db.session.commit()
        return {"message": "{} row(s) deleted".format(num_rows_deleted)}

    @staticmethod
    def generate_hash(password: str) -> str:
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password: str, hashed_password: str) -> bool:
        return sha256.verify(password, hashed_password)

    def change_password(self, new_hashed_password: str) -> None:
        if new_hashed_password != self.password:
            self.password = new_hashed_password
            db.session.commit()
        else:
            raise Exception("Passwords should not match")

    def change_login(self, new_login: str) -> None:
        if new_login != self.login:
            if not self.find_by_login(new_login):
                self.login = new_login
                db.session.commit()
            else:

                # TODO: вынести сообщения в константы
                raise Exception("The login is already occupied!")
        else:
            raise Exception("Logins should not match!")
