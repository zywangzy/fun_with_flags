"""Main entrypoint of RESTful API service."""
from flask import Flask, jsonify

from funwithflags.gateways import make_context
from funwithflags.use_cases import signup


context = make_context()
app = Flask(__name__)


def json_response(code, message, data):
    """Helper function of Flask to return json response. Will return a json object with structure of
    {"code": code, "msg": message, "data": data}, e.g. {"code": 200, "msg": "OK", "data": 1}.
    """
    return jsonify(code=code, msg=message, data=data)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/signup')
def api_signup(request):
    user_id = signup(request, context)
    if user_id == -1:
        return json_response(500, "Signup failed", "Internal error")
    else:
        return json_response(200, "OK", f"user_id={user_id}")


def main():
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
