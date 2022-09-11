from typing import Union

from core.config import config
from db.cache.base import BaseCache
from redis import Redis  # typing: ignore
from redis.client import Pipeline


class RedisCache(BaseCache):
    def get(self, key: str, **kwargs: str) -> str:
        return self.connection.get(f"{key}")

    def set_token(self, key: str, expire: int, value: Union[bytes, str]) -> None:
        self.connection.setex(name=f"{key}", time=expire, value=f"{value}")  # typing:ignore

    def pipeline(self, **kwargs: str) -> Pipeline:
        return self.connection.pipeline()


# TODO: добавить redis к config
redis_cache = RedisCache(
    connection=Redis(
        host=config.REDIS_DSN.host, port=config.REDIS_DSN.port, db=0, decode_responses=True, charset="utf-8"
    )
)
