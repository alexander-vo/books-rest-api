from typing import List

from pymongo import UpdateOne
from flask_pymongo import PyMongo

mongo = PyMongo()


def get_book(search_filter: dict) -> dict:
    """
    Search book by id in the database
    :param search_filter: filter for book search
    :return: book or None
    """
    return mongo.db.books.find_one(search_filter)


def get_books(search_filter: dict, sort: dict, pagination: dict) -> List[dict]:
    """
    Find books by search params in search_filter.
    Sort films by selected field and order in sort
    Paginate through books using pagination
    :param search_filter:
    :param sort:
    :param pagination:
    :return: books
    """
    skip = pagination['page_size'] * (pagination['page'] - 1)
    cursor = mongo.db.books.find(search_filter)
    cursor.sort(sort)
    cursor.skip(skip).limit(pagination['page_size'])
    return list(cursor)


def save_books(books: List[dict]) -> dict:
    """
    Save new books entries and update already existing ones
    :param books:
    :return: inserted books ids
    """
    # Creating list of operations for bulk update operation
    # upsert=True perform an insert if no documents match the filter
    operations = [UpdateOne({'_id': book['_id']}, book, upsert=True) for book in books]
    bulk_results = mongo.db.books.bulk_write(operations)
    return {
        'inserted': bulk_results.upserted_ids,
        'updated': bulk_results.modified_count
    }
