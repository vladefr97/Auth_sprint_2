from db.cache.base import BaseCache

from .instances.redis import redis_cache


def get_cache_instance() -> BaseCache:
    return redis_cache
