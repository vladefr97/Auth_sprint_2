from typing import Dict, Type

from flask import request

from .blueprint import oauth_blueprint
from .client import OAuthClient, OAuthClientName
from .clients.yandex import YandexOAuthClient

OAuthClients: Dict[str, Type[OAuthClient]] = {OAuthClientName.YANDEX.value: YandexOAuthClient}


@oauth_blueprint.route("/login/<provider>")
def provider_login(provider: str):
    oauth_client = OAuthClients[provider]()
    return oauth_client.get_redirect_uri()


# TODO: привести к формату api/v1?
@oauth_blueprint.route("/auth/<provider>")
def auth_provider(provider: str):
    oauth_client = OAuthClients[provider]()
    return oauth_client.get_user_info(request=request)
