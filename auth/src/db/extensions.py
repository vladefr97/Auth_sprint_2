from core.config import SQLALCHEMY_DATABASE_URI, config
from db.connection import db
from flask import Flask
from flask_migrate import Migrate, upgrade

from .models.user import User  # pylint: disable=W0611 # noqa
from .models.userrole import UserRole  # pylint: disable=W0611 # noqa

migrate = Migrate()


def init_db(app: Flask) -> None:
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.sqlalchemy_track_modifications
    db.init_app(app)
    app.app_context().push()
    db.create_all()


def init_migrate(app: Flask) -> None:
    migrate.init_app(app, db)
