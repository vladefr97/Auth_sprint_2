from pydantic import BaseModel


class YandexUserInfoSchema(BaseModel):
    id: str
    login: str
    client_id: str
    default_email: str
    emails: list[str]
    psuid: str
