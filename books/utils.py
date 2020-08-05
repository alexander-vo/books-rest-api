import requests
from typing import List


URL = 'https://www.googleapis.com/books/v1/volumes'
BOOKS_PER_PAGE = 40


def get_new_books_by_query(query: str) -> List[dict]:
    request_query = {
        'q': query,
        'langRestrict': 'en',
        'maxResults': BOOKS_PER_PAGE,
        'startIndex': 0
    }
    books = []
    response = requests.get(URL, params=request_query).json()
    while 'items' in response and response['items']:
        books.extend([parse_book(book) for book in response['items']])
        request_query['startIndex'] += BOOKS_PER_PAGE
        response = requests.get(URL, params=request_query).json()
    return books


def parse_book(book: dict) -> dict:
    return {
        '_id': book['id'],
        'title': book['volumeInfo'].get('title', ''),
        'authors': book['volumeInfo'].get('authors', ''),
        'published_date': book['volumeInfo'].get('publishedDate', ''),
        'categories': book['volumeInfo'].get('categories', []),
        'average_rating': book['volumeInfo'].get('averageRating', 0),
        'ratings_count': book['volumeInfo'].get('ratingsCount', 0),
        'thumbnail': book['volumeInfo'].get('imageLinks', {}).get('thumbnail', '')
    }
