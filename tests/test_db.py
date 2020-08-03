from config import TestingConfig
from books.db import mongo


# client var doesn't use but needed for fixture triggering
def test_db_name(client):
    """Testing connected Database name"""
    assert mongo.db.name == TestingConfig.MONGO_DB_NAME
