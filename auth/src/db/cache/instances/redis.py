from typing import Union

import os

from core.config import cache
from db.cache.base import BaseCache
from redis import Redis

# TODO: вынести настройки в pydantic config

REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))


class RedisCache(BaseCache):
    def get(self, key: str, **kwargs):
        return self.connection.get(f"{key}")

    def set_token(self, key: str, expire: int, value: Union[bytes, str]):
        self.connection.setex(name=f"{key}", time=expire, value=f"{value}")

    def pipeline(self, **kwargs):
        return self.connection.pipeline()


redis_cache = RedisCache(
    connection=Redis(host=cache.host, port=cache.port, db=0, decode_responses=True, charset="utf-8")
)
