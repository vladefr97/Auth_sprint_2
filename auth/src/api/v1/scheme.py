from typing import List, Optional

import orjson
from pydantic import BaseModel as PydanticBaseModel


def orjson_dumps(value, *, default):  # type: ignore
    return orjson.dumps(value, default=default).decode()


class BaseModel(PydanticBaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        allow_population_by_field_name = True


class UserHistoryScheme(BaseModel):
    user_agent: str
    ip_address: str
    url: Optional[str]
    timestamp: str


class UserHistoryPaginationScheme(BaseModel):
    has_next: bool
    has_prev: bool
    items: Optional[List[UserHistoryScheme]]
    next_num: Optional[int]
    page: int
    pages: int
    per_page: int
    prev_num: Optional[int]
