from __future__ import annotations

from typing import Dict

from datetime import datetime

from db.relational.connection import db
from db.relational.models.mixins import UUIDMixin
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID


class UserHistoryMixin(UUIDMixin):
    user_agent = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(20), nullable=False)
    url = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class UserHistory(db.Model, UserHistoryMixin):
    __tablename__ = "user_history"
    __table_args__ = {"extend_existing": True, "schema": "auth"}

    user_id = db.Column(
        "user_id", UUID(as_uuid=True), db.ForeignKey("auth.user.id", ondelete="cascade"), nullable=False
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f"<User {self.user_id} logged in {self.timestamp}>"

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls) -> dict[str, list[dict[str, str]]]:
        def to_json(user_history: UserHistory) -> Dict[str, str]:
            return {
                "user_id": str(user_history.user_id),
                "user_agent": user_history.user_agent,
                "ip_address": user_history.ip_address,
                "url": user_history.url,
                "timestamp": user_history.timestamp.isoformat(),
            }

        return {"user_history": [to_json(x) for x in UserHistory.query.all()]}

    @classmethod
    def delete_all(cls) -> Dict[str, str]:
        # TODO: добавить try, except
        num_rows_deleted = db.session.query(cls).delete()
        db.session.commit()
        return {"message": "{} row(s) deleted".format(num_rows_deleted)}


class UserHistoryTemp(db.Model, UserHistoryMixin):
    __tablename__ = "user_history_temp"
    __table_args__ = UniqueConstraint("id", "timestamp"), {
        "extend_existing": True,
        "schema": "auth",
        "postgresql_partition_by": "RANGE (timestamp)",
    }

    user_id = db.Column("user_id", UUID(as_uuid=True), nullable=False)
