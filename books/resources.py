from books import db
from books.utils import get_new_books_by_query
from flask_restful import Resource, abort, reqparse


class Books(Resource):

    # Creating settings for books endpoint query args
    parser = reqparse.RequestParser()
    parser.add_argument('published_date', type=str, trim=True)
    parser.add_argument('author', action='append', dest='authors')
    parser.add_argument('sort', type=str, trim=True)
    parser.add_argument('page', type=int, default=1)
    parser.add_argument('page_size', type=int, default=10)

    def get(self):
        args = self.parser.parse_args()

        # Creating pagination dict for books
        pagination = {'page': args['page'], 'page_size': args['page_size']}

        # Creating sort dict for published_date field if args['sort'] exists
        # else sort will be an None
        sort = args['sort'] and ('published_date', -1 if args['sort'].startswith('-') else 1)

        # Adding filter params if exists
        search_filter = {}
        if args['authors']:
            search_filter.update({'authors': {'$all': args['authors']}})
        if args['published_date']:
            search_filter.update({'published_date': args['published_date']})

        books = db.get_books(search_filter, sort, pagination)
        return {'data': books}


class Book(Resource):

    def get(self, book_id):
        # Search book by id
        result = db.get_book({'_id': book_id})
        if not result:
            # Raise 404 error if no book
            abort(404, data=[], message=f'No book with id: {book_id}')
        return {'data': [result]}


class AddBooks(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('q', type=str, required=True, location='json', help='q param need to be defined')

    def post(self):
        args = self.parser.parse_args()
        # Getting books from Google books API
        books = get_new_books_by_query(args['q'])
        # Saving new books
        result = db.save_books(books)
        return {'data': [result]}, 201
