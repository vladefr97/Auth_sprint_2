from pydantic import BaseModel
from pydantic_factories import ModelFactory


class FakeUser(BaseModel):
    login: str
    password: str


class FakeUserFactory(ModelFactory):
    __model__ = FakeUser
