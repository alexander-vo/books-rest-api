from books import db
from flask_restful import Resource, abort, reqparse


class Books(Resource):

    # Creating settings for books endpoint query args
    parser = reqparse.RequestParser()
    parser.add_argument('published_date', type=str, trim=True)
    parser.add_argument('authors', action='append')
    parser.add_argument('sort', type=str, trim=True)
    parser.add_argument('page', type=int, default=1)
    parser.add_argument('page_size', type=int, default=10)

    def get(self):
        args = self.parser.parse_args()

        # Creating pagination dict for books
        pagination = {'page': args['page'], 'page_size': args['page_size']}

        # Creating sort dict for published_date field if args['sort'] exists
        # else sort will be an empty dict
        sort = {} if not args['sort'] else \
            {'published_date': 1 if args['sort'].startswith('+') else -1}

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
        result = db.get_book({'_id': book_id})
        if not result:
            abort(404, data=[], message=f'No book with id: {book_id}')
        return {'data': [result]}
