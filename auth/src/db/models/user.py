from __future__ import annotations

from typing import Dict, List

from db.connection import db
from db.models.mixins import TimeStampedMixin, UUIDMixin
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model, UUIDMixin, TimeStampedMixin):
    # TODO: вынести названия таблиц и схем в константы
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True, "schema": "auth"}

    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    # TODO: заменить строковые названия таблицы
    user_role = db.Column(UUID(as_uuid=True), db.ForeignKey("auth.role.id", ondelete="cascade"))

    def __init__(self, login: str = login, password: str = password, user_role: UUID = user_role) -> None:
        self.login = login
        self.password = password
        self.user_role = user_role

    def __repr__(self) -> str:
        return f"<User {self.login}>"

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @property
    def identity(self) -> str:
        """
        *Required Attribute or Property*
        flask-praetorian requires that the user class has an ``identity`` instance
        attribute or property that provides the unique id of the user instance
        """
        return str(self.id)

    @classmethod
    def find_by_login(cls, login: str) -> User:
        return cls.query.filter_by(login=login).first()

    @classmethod
    def find_by_id(cls, user_id: str) -> User:
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def return_all(cls) -> Dict[str, List[Dict[str, str]]]:
        def to_json(user: User) -> Dict[str, str]:
            return {"login": user.login, "password": user.password}

        return {"users": [to_json(x) for x in User.query.all()]}

    @classmethod
    def delete_all(cls) -> Dict[str, str]:
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
