from typing import Type
from flask import Flask
from config import Config


def create_app(app_config: Type[Config] = Config) -> Flask:
    """
    Creating a flask application with configs
    :param app_config: config class
    :return: Flask object
    """
    app = Flask(__name__)
    app.config.from_object(app_config())
    return app
