"""Main entrypoint of RESTful API service."""
from flask import Flask

from funwithflags.entities import make_context
from funwithflags.use_cases import signup


context = make_context()
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/signup')
def api_signup(request):
    signup(request, context)


if __name__ == '__main__':
    app.run()
