from flask import current_app as app
from flask_restful import Resource, abort

books = [
    {
        'id': '1'
        , 'title': 'Harry Potter and the Order of the Phoenix'
    },
    {
        'id': '2'
        , 'title': 'Hobbit'
    },
    {
        'id': '3'
        , 'title': 'Star Wars'
    },
    {
        'id': '4'
        , 'title': '1984'
    },
    {
        'id': '5'
        , 'title': 'Old Man and Sea'
    },
]


class Books(Resource):

    def get(self):
        return {'data': books}


class Book(Resource):

    def get(self, id):
        result = [book for book in books if book['id'] == id]
        if not result:
            abort(404, data=[], message=f'No book with id: {id}')
        return {'data': [result[0]]}
