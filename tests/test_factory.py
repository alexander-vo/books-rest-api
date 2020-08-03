from books import create_app
from config import TestingConfig


def test_config():
    assert not create_app().testing
    assert create_app(TestingConfig).testing
