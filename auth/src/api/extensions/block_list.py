from db.cache import get_cache_instance
from db.cache.base import BaseCache

jwt_blocklist = get_cache_instance()


def get_blocklist() -> BaseCache:
    return jwt_blocklist
