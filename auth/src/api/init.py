from flask import Flask
from flask_restful import Api

from .extensions import init_extensions
from .urls import urls


def init_api(app: Flask) -> None:
    api = Api(app)
    init_extensions(app)
    _set_api_resources(api)


def _set_api_resources(api: Api) -> None:
    for (resource, url) in urls:
        api.add_resource(resource, url)
