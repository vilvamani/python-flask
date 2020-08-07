# Importing flask module in the project is mandatory 
# An object of Flask class is our WSGI application. 
from flask import Flask, request, jsonify


# Flask constructor takes the name of  
# current module (__name__) as argument. 
app = Flask(__name__)
app.config["DEBUG"] = True

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
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call  
# the associated function.
# ‘/’ URL is bound with home() function.
@app.route('/', methods=['GET'])
def home():
    headers = request.headers
    auth = headers.get("X-Api-Key")
    if auth == 'asoidewfoef':
        return jsonify({"message": "OK: Authorized"}), 200
    else:
        return jsonify({"message": "ERROR: Unauthorized"}), 401

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/books/all', methods=['GET'])
def get_all_books():
    return jsonify(books)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

@app.route('/api/v1/resources/books/<int:book_id>', methods=['GET'])
def get_book_id(book_id):
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0:
        return "Error: No id field provided. Please specify an id."
    return jsonify({'task': book[0]})

# ‘/help’ URL is bound with help() function.
@app.route('/help')
def help():
    return 'Connect with vilvamani007@gmail.com'

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server. 
    app.run(host='0.0.0.0')
