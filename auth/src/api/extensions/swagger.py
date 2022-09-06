from core.config import settingsSwagger, templateSwagger
from flasgger import Swagger
from flask import Flask

swagger = Swagger(template=templateSwagger)


def init_swagger(app: Flask) -> None:
    swagger.init_app(app)
    app.config["SWAGGER"] = settingsSwagger
