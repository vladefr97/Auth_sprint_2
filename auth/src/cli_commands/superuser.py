from typing import Callable

import click
from core.models import DefaultUserRole
from db.models import User
from db.models.userrole import UserRole
from flask import Flask


def get_superuser_creation_command(app: Flask) -> Callable:  # type: ignore
    @app.cli.command("create-superuser")
    @click.argument("login")
    @click.argument("password")
    def create_superuser(login: str, password: str) -> None:
        superuser_login = login

        if not User.find_by_login(superuser_login):
            superuser_role_type = UserRole.get_role(DefaultUserRole.SUPERUSER.value)
            superuser_password = password
            superuser = User(
                login=superuser_login, password=User.generate_hash(superuser_password), user_role=superuser_role_type.id
            )
            superuser.save_to_db()

    return create_superuser
