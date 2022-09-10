import datetime
from functools import wraps
from http import HTTPStatus

from db.cache import get_cache_instance
from flask import request

cache = get_cache_instance()

# TODO: вынести в переменные
RATE_LIMIT = 1000
RATE_INTERVAL = 60


def rate_limit(limit=RATE_LIMIT, interval=RATE_INTERVAL):
    def rate_limit_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = f"limit::{request.remote_addr}:{datetime.datetime.now().minute}"
            current_requests_count = cache.get(key=key)

            if current_requests_count and int(current_requests_count) >= limit:
                return {
                           "message": f"Too many requests. Limit {limit} in {interval} seconds",
                       }, HTTPStatus.TOO_MANY_REQUESTS

            pipe = cache.pipeline()
            pipe.incr(key, 1)
            pipe.expire(key, interval + 1)
            pipe.execute()

            return func(*args, **kwargs)

        return wrapper

    return rate_limit_decorator
