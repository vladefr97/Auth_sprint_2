from pydantic import BaseModel


class JWTTokens(BaseModel):
    access_token: str
    refresh_token: str
