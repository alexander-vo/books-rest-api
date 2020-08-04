import pytest
from flask import Flask

from books import create_app
from books.db import mongo
from config import TestingConfig


@pytest.fixture
def app() -> Flask:
    """Yield fixture app and close db connection"""
    yield create_app(TestingConfig)
    mongo.cx.close()


@pytest.fixture
def client(app: Flask) -> Flask:
    """Returns app test client"""
    return app.test_client()
