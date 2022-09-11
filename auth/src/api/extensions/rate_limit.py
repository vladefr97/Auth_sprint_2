from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from core.config import config

rate_limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1 per day"],
    storage_uri=config.REDIS_DSN,
)


def init_rate_limiter(app: Flask):
    rate_limiter.init_app(app)
