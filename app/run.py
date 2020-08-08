from flask import Flask, request, make_response, jsonify
from flask_restful import Api
from .book import AllBooks, Book, NewBook

app = Flask(__name__)
app.config["DEBUG"] = True

api = Api(app)
api.add_resource(AllBooks, '/api/v1/books')
api.add_resource(Book, '/api/v1/book/<int:book_id>')
api.add_resource(NewBook, '/api/v1/book')

@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({'error': 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'}), 404)


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call  
# the associated function.
# ‘/’ URL is bound with home() function.
@app.route('/', methods=['GET'])
def home():
    return make_response(jsonify({'Message': 'Python Flask App'}))

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server. 
    app.run(host='0.0.0.0')