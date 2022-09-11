import os
from http import HTTPStatus

from api.v1.blueprints.oauth.client import OAuthClient, OAuthClientCredentials, OAuthClientName
from api.v1.blueprints.oauth.schema.yandex import YandexUserInfoSchema


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

    def get_user_info(self, request=None) -> tuple[dict, HTTPStatus]:
        self.client.authorize_access_token()

        user_info_response = self.client.get(self.credentials.userinfo_endpoint).json()
        user_info = YandexUserInfoSchema(**user_info_response)
        return super().provide_user_info(
            login=user_info.login,
            email=user_info.emails[0] if len(user_info.emails) else "",
            social_id=user_info.id,
            social_name=self.credentials.provider.value,
        )
