from typing import Dict

import os
from http import HTTPStatus

from api.v1.blueprints.oauth.client import OAuthClient, OAuthClientCredentials, OAuthClientName
from api.v1.blueprints.oauth.schema.yandex import YandexUserInfoSchema
from api.v1.blueprints.oauth.utils import attach_social_account_to_user, register_user_if_not_exists
from api.v1.utils import create_jwt_tokens
from db.relational.models.userrole import UserRole


class YandexOAuthClientCredentials(OAuthClientCredentials):
    def set_credentials(self) -> None:
        self.provider = OAuthClientName.YANDEX
        self.client_id = os.getenv("YANDEX_CLIENT_ID")
        self.client_secret = os.getenv("YANDEX_CLIENT_SECRET")
        # TODO: вынести оставшиеся поля либо в словарь, либо в переменные среды
        self.access_token_url = "https://oauth.yandex.ru/token"
        self.authorize_url = "https://oauth.yandex.ru/authorize/"
        self.userinfo_endpoint = "https://login.yandex.ru/info"
        self.client_kwargs = {"scope": "login:email"}


class YandexOAuthClient(OAuthClient):
    def __init__(self):
        super().__init__(YandexOAuthClientCredentials())

    def get_user_info(self, request=None) -> tuple[Dict[str, str], HTTPStatus]:
        self.client.authorize_access_token()
        user_info_response = self.client.get(self.credentials.userinfo_endpoint).json()
        user_info = YandexUserInfoSchema(**user_info_response)
        registered_user = register_user_if_not_exists(
            login=user_info.login, email=user_info.emails[0] if len(user_info.emails) else ""
        )
        attach_social_account_to_user(
            social_id=user_info.id, social_name=self.credentials.provider.value, user=registered_user
        )

        user_role_model = UserRole.find_by_id(role_id=registered_user.user_role)
        jwt_tokens = create_jwt_tokens(user_login=registered_user.login, user_role=user_role_model.role_type)
        response = jwt_tokens.dict()
        response["message"] = f"Logged in as {registered_user.login} - {registered_user.email}"

        return response, HTTPStatus.OK
