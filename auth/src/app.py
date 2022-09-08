from api import init_api  # noqa
from cli_commands import get_superuser_creation_command
from core.config import config
from core.tracer import configure_tracer
from db import init_db, init_migrate  # noqa
from flask import Flask, make_response, request  # noqa
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from scripts import create_default_user_roles  # noqa

configure_tracer()


def main() -> Flask:
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = config.jwt_secret_key
    init_db(app)
    init_migrate(app)
    init_api(app)
    create_default_user_roles()
    app.cli.add_command(get_superuser_creation_command(app))
    FlaskInstrumentor().instrument_app(app)
    return app


app = main()


if __name__ == "__main__":
    app.run(debug=config.debug)
