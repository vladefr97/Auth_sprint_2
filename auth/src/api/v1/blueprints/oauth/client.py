from typing import Dict

from abc import ABC, abstractmethod
from enum import Enum
from http import HTTPStatus

from db.relational.models import User
from db.relational.models.social_account import SocialAccount
from db.relational.models.userrole import UserRole
from flask import url_for

from ...utils import create_jwt_tokens
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

    def provide_user_info(
        self, login: str, email: str, social_id: str, social_name: str
    ) -> tuple[Dict[str, str], HTTPStatus]:
        registered_user = User.find_by_login_or_email(login=login, email=email)
        if not registered_user:
            registered_user = User.save_user_with_default_role(
                login=login, email=email, password=User.get_random_user_password()
            )
        SocialAccount.attach_social_account_to_user(social_id=social_id, social_name=social_name, user=registered_user)

        user_role_model = UserRole.find_by_id(role_id=registered_user.user_role)
        jwt_tokens = create_jwt_tokens(user_login=registered_user.login, user_role=user_role_model.role_type)
        response = jwt_tokens.dict()
        response["message"] = f"Logged in as {registered_user.login} - {registered_user.email}"
        return response, HTTPStatus.OK

    @abstractmethod
    def get_user_info(self, request=None) -> tuple[Dict[str, str], HTTPStatus]:
        ...

    def get_redirect_uri(self) -> str:
        # TODO: сделать нормально без префикса oauth_blueprint
        uri = url_for("oauth_blueprint.auth_provider", _external=True, provider=self.credentials.provider.value)

        return self.client.authorize_redirect(uri)
