# from db.cache import BaseCache
from .instances.redis import redis_cache


def get_cache_instance():
    return redis_cache
