from typing import Any, Dict

from abc import ABC, abstractmethod
from enum import Enum

from flask import url_for

from .extensions import oauth


class OAuthClientName(Enum):
    YANDEX = "yandex"


class OAuthClientCredentials(ABC):
    provider: OAuthClientName
    client_id: str
    client_secret: str
    access_token_url: str
    authorize_url: str
    userinfo_endpoint: str
    client_kwargs: Dict[str, str]

    @abstractmethod
    def set_credentials(self) -> None:
        ...


class OAuthClient(ABC):
    credentials: OAuthClientCredentials

    def __init__(self, credentials: OAuthClientCredentials):
        self.credentials = credentials
        self.credentials.set_credentials()
        self.register_client_service()

    def register_client_service(self) -> None:
        self.client = oauth.register(
            name=self.credentials.provider.value,
            client_id=self.credentials.client_id,
            client_secret=self.credentials.client_secret,
            access_token_url=self.credentials.access_token_url,
            access_token_params=None,
            authorize_url=self.credentials.authorize_url,
            authorize_params=None,
            api_base_url="",
            userinfo_endpoint=self.credentials.userinfo_endpoint,
            client_kwargs=self.credentials.client_kwargs,
        )

    @abstractmethod
    def get_user_info(self, request=None) -> Dict[str, Any]:
        ...

    def get_redirect_uri(self) -> str:
        # TODO: сделать нормально без префикса oauth_blueprint
        uri = url_for("oauth_blueprint.auth_provider", _external=True, provider=self.credentials.provider.value)

        return self.client.authorize_redirect(uri)
