from typing import List

from pydantic import BaseModel


class YandexUserInfoSchema(BaseModel):
    id: str
    login: str
    client_id: str
    default_email: str
    emails: List[str]
    psuid: str
