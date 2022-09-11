from api import init_api  # noqa
from cli_commands import get_superuser_creation_command
from core.config import config
from core.tracer import init_tracer
from db import init_db, init_migrate  # noqa
from flask import Flask  # noqa
from scripts import create_default_user_roles  # noqa


def main() -> Flask:
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
    app.config["SECRET_KEY"] = config.APP_SECRET_KEY
    init_db(app)
    init_migrate(app)
    init_api(app)
    create_default_user_roles()
    app.cli.add_command(get_superuser_creation_command(app))
    init_tracer(app)
    return app


app = main()

if __name__ == "__main__":
    app.run(debug=config.DEBUG,ssl_context="adhoc")
