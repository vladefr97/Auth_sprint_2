import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID

from db.connection import db


class UUIDMixin:
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )


class TimeStampedMixin:
    __abstract__ = True

    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )


class SavableMixin:
    __abstract__ = True

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
