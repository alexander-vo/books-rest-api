from flask import Flask, Response, make_response
from flask_restful import Api
from typing import Type

from config import Config
from books.db import mongo
from books.resources import Books, Book


def create_app(app_config: Type[Config] = Config) -> Flask:
    """
    Creating a flask application with configs
    :param app_config: config class
    :return: Flask object
    """
    app = Flask(__name__)
    app.config.from_object(app_config())

    # Mongo init app
    mongo.init_app(app)

    # Creating API object for the Flask app
    api = Api(app, prefix='/api')

    # Creating custom template for API responses
    # Could also map codes to status_message field like 'success' or 'failure'
    @api.representation('application/json')
    def formatting_response(data, code, headers=None) -> Response:
        body = {'status': code, **data}
        response = make_response(body, code)
        response.headers.extend(headers or {})
        return response

    # Adding api resources
    api.add_resource(Books, '/books/')
    api.add_resource(Book, '/books/<string:book_id>')

    return app
