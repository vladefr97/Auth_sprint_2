from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def get_db_instance() -> SQLAlchemy:
    return db
