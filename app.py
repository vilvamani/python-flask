# Importing flask module in the project is mandatory 
# An object of Flask class is our WSGI application. 
from flask import Flask

# Flask constructor takes the name of  
# current module (__name__) as argument. 
app = Flask(__name__)


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call  
# the associated function.
# ‘/’ URL is bound with home() function.
@app.route('/')
def home():
    return 'Hello World'

# ‘/help’ URL is bound with help() function.
@app.route('/help')
def help():
    return 'Connect with vilvamani007@gmail.com'

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server. 
    app.run(debug=True, host='0.0.0.0')