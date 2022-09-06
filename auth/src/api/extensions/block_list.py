from core.config import cache
from redis import StrictRedis  # type: ignore

jwt_blocklist = StrictRedis(host=cache.host, port=cache.port, db=0, decode_responses=True)


def get_blocklist() -> StrictRedis:
    return jwt_blocklist
