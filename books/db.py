from typing import List, Optional

from pymongo import UpdateOne
from flask_pymongo import PyMongo

from books.models import Book, Pagination, SaveBooksResults

mongo = PyMongo()


def get_book(search_filter: dict) -> Optional[Book]:
    """
    Search book by id in the database
    """
    book = mongo.db.books.find_one(search_filter)
    return Book(**book) if book else None


def get_books(search_filter: dict, sort: tuple, pagination: Pagination = Pagination()) -> List[Book]:
    """
    Find books by search params in 'search_filter'.
    Sort films by 'published_date' field and order in 'sort'
    Paginate through books using 'pagination'
    """
    cursor = mongo.db.books.find(search_filter)

    if sort:
        cursor.sort(*sort)

    skip = pagination.page_size * (pagination.page - 1)
    cursor.skip(skip).limit(pagination.page_size)

    return [Book(**book) for book in cursor]


def save_books(books: List[Book]) -> SaveBooksResults:
    """
    Save new books entries and update already existing ones
    """
    if not books:
        return SaveBooksResults()

    # Creating list of operations for bulk update operation
    # upsert=True perform an insert if no documents match the filter
    operations = [UpdateOne({'_id': book.id}, {'$set': book.dict(by_alias=True)}, upsert=True) for book in books]
    bulk_results = mongo.db.books.bulk_write(operations)

    return SaveBooksResults(
        inserted_ids=list(bulk_results.upserted_ids.values()),
        updated_count=bulk_results.modified_count
    )
