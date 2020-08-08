from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_httpauth import HTTPBasicAuth


# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'year_published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'year_published': '1975'}
]

parser = reqparse.RequestParser()
parser.add_argument('title', help = 'This field cannot be blank', required = True)
parser.add_argument('author', help = 'This field cannot be blank', required = True)
parser.add_argument('first_sentence', help = 'This field cannot be blank', required = True)
parser.add_argument('year_published', help = 'This field cannot be blank', required = True)

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'vilva':
        return 'devops'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


class AllBooks(Resource):
    @auth.login_required
    def get(self):
        return jsonify(books)

class Book(Resource):
    @auth.login_required
    def get(self, book_id):
        book = [book for book in books if book['id'] == book_id]
        if len(book) == 0:
            return "Error: No id field provided. Please specify an id."
        return jsonify({'Book': book[0]})

    @auth.login_required
    def delete(self, book_id):
        book = [book for book in books if book['id'] == book_id]
        if len(book) == 0:
            return "Error: Book not found"
        books.remove(book[0])
        return jsonify({'result': True})

class NewBook(Resource):
    @auth.login_required
    def post(self):
        data = parser.parse_args()

        book = {
            'id': books[-1]['id'] + 1,
            'title': data['title'],
            'author': data['author'],
            'first_sentence': data['first_sentence'],
            'published': data['year_published']
        }

        books.append(book)
        return {'Book': book}, 201
