from core.config import config
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

rate_limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per day"],
    storage_uri=config.REDIS_DSN,
)


def init_rate_limiter(app: Flask) -> None:
    rate_limiter.init_app(app)
