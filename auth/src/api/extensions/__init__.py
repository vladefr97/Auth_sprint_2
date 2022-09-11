from api.v1.blueprints.oauth import init_oauth
from flask import Flask

from .jwt import init_jwt
from .rate_limit import init_rate_limiter
from .swagger import init_swagger


def init_extensions(app: Flask) -> None:
    init_jwt(app)
    init_swagger(app)
    init_oauth(app)
    init_rate_limiter(app)


__all__ = ["init_extensions"]
