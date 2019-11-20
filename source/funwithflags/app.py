"""Main entrypoint of RESTful API service."""
from http import HTTPStatus as status
import logging

from flask import Flask
from flask import jsonify, request, make_response

from funwithflags.definitions import SignupRequest
from funwithflags.definitions import DatabaseQueryError
from funwithflags.gateways import Context
from funwithflags.use_cases import signup

logger = logging.getLogger(__name__)
context = Context()
app = Flask(__name__)


def app_response(code, message, **data):
    """Helper function of Flask to return json response. Will return a json object with structure of
    {"code": code, "msg": message, "data": data}, e.g. {"code": 200, "msg": "OK", "data": 1}.
    """
    return make_response(jsonify(message=message, **data), code)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/signup", methods=["GET"])
def api_signup():
    try:
        content = request.get_json(force=True)
        signup_request = SignupRequest(
            username=content["username"],
            nickname=content["nickname"],
            email=content["email"],
            password=content["password"],
        )
        user_id = signup(signup_request, context)
        return app_response(status.CREATED, message="OK", user_id=user_id)
    except KeyError:
        return app_response(status.BAD_REQUEST, message="Invalid request")
    except DatabaseQueryError:
        return app_response(status.CONFLICT, message="Conflict user")
    except Exception:
        return app_response(status.INTERNAL_SERVER_ERROR, message="Internal error")


def main():
    app.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
