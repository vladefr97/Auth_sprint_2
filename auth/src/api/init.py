from api.v1.blueprints.oauth import oauth_blueprint
from flask import Flask
from flask_restful import Api

from .extensions import init_extensions
from .urls import urls
from .v1.blueprints.oauth.routes import auth_provider, provider_login


def init_api(app: Flask) -> None:
    api = Api(app)
    init_extensions(app)
    _set_api_resources(api)
    _init_api_blueprints(app)


def _init_api_blueprints(app: Flask) -> None:
    app.register_blueprint(oauth_blueprint)


def _set_api_resources(api: Api) -> None:
    for (resource, url) in urls:
        api.add_resource(resource, url)
