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


def get_books(search_filter: dict, sort: tuple, pagination: dict) -> List[dict]:
    """
    Find books by search params in search_filter.
    Sort films by selected field and order in sort
    Paginate through books using pagination
    :param search_filter:
    :param sort:
    :param pagination:
    :return: books
    """
    skip = pagination.get('page_size', 10) * (pagination.get('page', 1) - 1)
    cursor = mongo.db.books.find(search_filter)
    if sort:
        cursor.sort(*sort)
    cursor.skip(skip).limit(pagination.get('page_size', 10))
    return list(cursor)


def save_books(books: List[dict]) -> dict:
    """
    Save new books entries and update already existing ones
    :param books:
    :return: inserted books ids and updated count
    """
    result = {
        'inserted_ids': [],
        'updated_count': 0
    }
    # Empty books leads to an empty operations list
    # what raise InvalidOperation exception
    if not books:
        return result
    # Creating list of operations for bulk update operation
    # upsert=True perform an insert if no documents match the filter
    operations = [UpdateOne({'_id': book['_id']}, {'$set': book}, upsert=True) for book in books]
    bulk_results = mongo.db.books.bulk_write(operations)
    result.update({
        'inserted_ids': list(bulk_results.upserted_ids.values()),
        'updated_count': bulk_results.modified_count
    })
    return result
