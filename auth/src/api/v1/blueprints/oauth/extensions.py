from authlib.integrations.flask_client import OAuth
from flask import Flask

oauth = OAuth()


def init_oauth(app: Flask):
    oauth.init_app(app)





