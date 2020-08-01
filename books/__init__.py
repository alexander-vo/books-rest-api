from typing import Type
from flask import Flask
from config import Config


def create_app(app_config: Type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(app_config)
    return app
