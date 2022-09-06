from flask import Flask

from .jwt import init_jwt
from .swagger import init_swagger


def init_extensions(app: Flask) -> None:
    init_jwt(app)
    init_swagger(app)


__all__ = ["init_extensions"]
