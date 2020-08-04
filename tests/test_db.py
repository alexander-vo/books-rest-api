import pytest

from config import TestingConfig
from books import db


# client var doesn't use but needed for fixture triggering
def test_db_name(client):
    """
    Testing connected Database name
    :param client: needed to init fixture
    :return:
    """
    assert db.mongo.db.name == TestingConfig.MONGO_DB_NAME


@pytest.mark.parametrize(
    'book_id, expected_title',
    [
        ('CSUeAQAAIAAJ', 'The Hobbit'),
        ('KY0BDObXftUC', 'Exploring J.R.R. Tolkien\'s The Hobbit'),
        ('8_YUAgAAQBAJ', 'The Hobbit, the Desolation of Smaug'),
        (None, None),
        ('some_random_string', None)
    ]
)
def test_get_book_method(book_id, expected_title):
    """
    Testing search by id. Comparing founded book title
    with extend one
    Tested id = None and some random string
    :param book_id:
    :param expected_title:
    :return:
    """
    book = db.get_book({'_id': book_id})
    title = book['title'] if book else None
    assert title == expected_title


@pytest.mark.parametrize(
    'published_date, authors, sort'
)
def test_get_books_method_search_and_sort(published_date, authors, sort):
    pass
