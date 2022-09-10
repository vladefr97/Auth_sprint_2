from __future__ import annotations

from typing import Dict

from datetime import datetime

from db.connection import db
from db.models.mixins import UUIDMixin, SavableMixin
from sqlalchemy.dialects.postgresql import UUID


class UserHistory(db.Model, UUIDMixin,SavableMixin):
    __tablename__ = "user_history"
    __table_args__ = {"extend_existing": True, "schema": "auth"}

    user_id = db.Column("user_id", UUID(as_uuid=True), db.ForeignKey("auth.user.id", ondelete="cascade"))
    user_agent = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(20))
    url = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(
        self, user_id: int = user_id, user_agent: str = user_agent, ip_address: str = ip_address, url: str = url
    ):
        self.user_id = user_id
        self.user_agent = user_agent
        self.ip_address = ip_address
        self.url = url

    def __repr__(self) -> str:
        return f"<User {self.user_id} logged in {self.timestamp}>"

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

    @classmethod
    def get_user_history(cls, user_id: str) -> dict[str, list[dict[str, str]]]:
        def to_json(user_history: UserHistory) -> Dict[str, str]:
            return {
                "user_id": str(user_history.user_id),
                "user_agent": user_history.user_agent,
                "ip_address": user_history.ip_address,
                "url": user_history.url,
                "timestamp": user_history.timestamp.isoformat(),
            }

        return {"user_history": [to_json(_) for _ in UserHistory.query.filter_by(user_id=user_id).all()]}
