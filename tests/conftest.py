import os
import json
import pytest

from flask import Flask

from books import create_app
from books.db import mongo
from config import TestingConfig

TESTS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))


@pytest.fixture(scope='session')
def app() -> Flask:
    """Yield fixture app and close db connection after tests end"""
    yield create_app(TestingConfig)
    mongo.cx.close()


@pytest.fixture(scope='session')
def client(app: Flask) -> Flask:
    """Returns app test client and loads test data from tests_books.json"""
    with open(os.path.join(TESTS_DIR, 'test_books.json'), 'r') as f:
        data = json.load(f)
    mongo.db.books.insert_many(data)
    yield app.test_client()
    mongo.db.books.remove()
