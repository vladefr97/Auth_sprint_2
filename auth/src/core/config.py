from typing import Any, Union

from datetime import timedelta

from pydantic import BaseSettings, Field, PostgresDsn, RedisDsn


class Config(BaseSettings):
    JWT_SECRET_KEY: str = Field(default="my_secret_key", env="JWT_SECRET_KEY")
    APP_SECRET_KEY: str = Field(default="app_secret_key", env="APP_SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = Field(default="True", env="SQLALCHEMY_TRACK_MODIFICATIONS")
    DEBUG: bool = Field(default="True", env="DEBUG")
    JAEGER_HOST: str = Field(default="localhost", env="JAEGER_HOST")
    JAEGER_PORT: int = Field(default="6831", env="JAEGER_PORT")
    REDIS_DSN: RedisDsn = Field(default="redis://user:pass@localhost:6379", env="REDIS_DSN")
    POSTGRES_DSN: PostgresDsn = Field(
        default="postgresql+psycopg2://app:123qwe@localhost:5432/movies_database", env="POSTGRES_DSN"
    )


config: Config = Config()

SQLALCHEMY_DATABASE_URI = config.POSTGRES_DSN

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
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1).seconds
