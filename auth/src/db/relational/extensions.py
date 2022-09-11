from core.config import SQLALCHEMY_DATABASE_URI, config
from db.relational.connection import db
from db.relational.models.social_account import SocialAccount  # pylint: disable=W0611 # noqa
from db.relational.models.user import User  # pylint: disable=W0611 # noqa
from db.relational.models.userrole import UserRole  # pylint: disable=W0611 # noqa
from flask import Flask
from flask_migrate import Migrate

migrate = Migrate()


def init_db(app: Flask) -> None:
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    db.init_app(app)
    app.app_context().push()


def init_migrate(app: Flask) -> None:
    migrate.init_app(app, db)
