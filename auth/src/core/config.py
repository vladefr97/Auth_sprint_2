from typing import Any, Union

from pydantic import BaseSettings, Field


class DBSettings(BaseSettings):
    HOST: str = Field(default="localhost", env="POSTGRES_HOST")
    PORT: str = Field(default="5432", env="POSTGRES_PORT")
    DB: str = Field(default="movies_database", env="POSTGRES_DB")
    PASSWORD: str = Field(default="123qwe", env="POSTGRES_PASSWORD")
    USER: str = Field(default="app", env="POSTGRES_USER")


class RedisSettings(BaseSettings):
    host: str = Field(default="localhost", env="REDIS_HOST")
    port: str = Field(default="6379", env="REDIS_PORT")


db: DBSettings = DBSettings()
cache: RedisSettings = RedisSettings()

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{db.USER}:{db.PASSWORD}@{db.HOST}:{db.PORT}/{db.DB}"


class Config(BaseSettings):
    jwt_secret_key: str = Field(default="my_secret_key", env="JWT_SECRET_KEY")
    app_secret_key:str = Field(default='app_secret_key',env="APP_SECRET_KEY")
    superuser_login: str = Field(default="su", env="SUPERUSER_LOGIN")
    superuser_password: str = Field(default="123qwe", env="SUPERUSER_PASSWORD")
    sqlalchemy_track_modifications: bool = Field(default="True", env="SQLALCHEMY_TRACK_MODIFICATIONS")
    debug: bool = Field(default="True", env="DEBUG")


config: Config = Config()


settingsSwagger: dict[str, int] = {
    "uiversion": 3,
}
templateSwagger: dict[str, Union[Any]] = {
    "openapi": "2.0.0",
    "info": {
        "title": "Auth service, Team 6",
        "description": "Sprint 6",
        "version": "1.0",
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme."
            ' Example: "Authorization: Bearer {token}"',
        }
    },
    "security": [{"Bearer": []}],
    "consumes": [
        "application/json",
    ],
    "produces": [
        "application/json",
    ],
}
