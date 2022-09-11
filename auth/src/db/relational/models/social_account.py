from db.relational.connection import db
from db.relational.models import User
from db.relational.models.mixins import TimeStampedMixin, UUIDMixin
from sqlalchemy.dialects.postgresql import UUID


class SocialAccount(db.Model, UUIDMixin, TimeStampedMixin):
    # TODO: вынести названия таблиц в один файл
    __tablename__ = "social_account"
    __table_args__ = {"extend_existing": True, "schema": "auth"}

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("auth.user.id"), nullable=False)

    social_id = db.Column(db.String(length=100), nullable=False)
    social_name = db.Column(db.String(length=100), nullable=False)
    db.UniqueConstraint(social_id, social_name)

    def __init__(self, user_id: UUID, social_id: str, social_name: str):
        self.user_id = user_id
        self.social_id = social_id
        self.social_name = social_name

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def attach_social_account_to_user(cls, social_name: str, social_id: str, user: User) -> None:
        if not SocialAccount.exists(user_id=user.id, social_id=social_id, social_name=social_name):
            SocialAccount(user_id=user.id, social_id=social_id, social_name=social_name).save_to_db()

    @classmethod
    def exists(cls, user_id: str, social_id: str, social_name: str) -> bool:
        return bool(cls.query.filter_by(user_id=user_id, social_id=social_id, social_name=social_name).first())

    def __repr__(self) -> str:
        return f"<SocialAccount {self.social_name}:{self.user_id}>"
