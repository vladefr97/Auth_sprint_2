from __future__ import annotations

from typing import Dict, List

from uuid import UUID

from db.connection import db
from db.models.mixins import UUIDMixin


class UserRole(db.Model, UUIDMixin):
    __tablename__ = "role"
    __table_args__ = {"extend_existing": True, "schema": "auth"}

    role_type = db.Column(db.String)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls) -> List[Dict[str, str]]:
        def to_json(user_role: UserRole) -> Dict[str, str]:
            return {"role": user_role.role_type, "id": str(user_role.id)}

        return [to_json(x) for x in UserRole.query.all()]

    @classmethod
    def delete_by_id(cls, role_id: UUID) -> None:
        cls.query.filter_by(id=role_id).delete()
        db.session.commit()

    @classmethod
    def get_role(cls, user_role_type: str) -> UserRole:
        return cls.query.filter_by(role_type=user_role_type).first()

    @classmethod
    def find_by_id(cls, role_id: UUID) -> UserRole:  # noqa
        return cls.query.filter_by(id=role_id).first()
