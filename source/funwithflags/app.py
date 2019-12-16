"""Main entrypoint of RESTful API service."""
from http import HTTPStatus as status
import logging

from flask import Flask
from flask import jsonify, request, make_response
from flasgger import swag_from, Swagger

from funwithflags.definitions import RegisterRequest
from funwithflags.definitions import BadRequestError, DatabaseQueryError
from funwithflags.gateways import Context
from funwithflags.use_cases import register

logger = logging.getLogger(__name__)
context = Context()
app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'Funwithflags API',
    'openapi': '3.0.2',
    'uiversion': 3,
    'schemes': [
        "https"
    ],
    'securitySchemes': {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
}
swagger = Swagger(app)


UNSUPPORTED = "Unsupported function"


def app_response(code, message, **data):
    """Helper function of Flask to return json response. Will return a json object with structure of
    {"code": code, "msg": message, "data": data}, e.g. {"code": 200, "msg": "OK", "data": 1}.
    """
    return make_response(jsonify(message=message, **data), code)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/user", methods=["GET"])
@swag_from("swagger_docs/user_read.yml")
def user_read(user_id):
    return app_response(status.FORBIDDEN, message=UNSUPPORTED)


@app.route("/user/register", methods=["POST"])
@swag_from("swagger_docs/user_register.yml")
def user_register():
    try:
        content = request.get_json(force=True)
        register_request = RegisterRequest(
            username=content["username"],
            nickname=content["nickname"],
            email=content["email"],
            password=content["password"],
        )
        user_id = register(register_request, context)
        return app_response(status.CREATED, message="OK", user_id=user_id)
    except (KeyError, BadRequestError):
        return app_response(status.BAD_REQUEST, message="Invalid request")
    except DatabaseQueryError:
        return app_response(status.CONFLICT, message="Conflict user")
    except Exception as e:
        logger.info(
            f'An exception happened when handling signup request "{content}": {e}'
        )
        return app_response(status.INTERNAL_SERVER_ERROR, message="Internal error")


@app.route("/user/login", methods=["POST"])
@swag_from("swagger_docs/user_login.yml")
def user_login():
    return app_response(status.FORBIDDEN, message=UNSUPPORTED)


@app.route("/user/logout", methods=["POST"])
@swag_from("swagger_docs/user_logout.yml")
def user_logout():
    return app_response(status.FORBIDDEN, message=UNSUPPORTED)


@app.route("/user/update", methods=["POST"])
@swag_from("swagger_docs/user_update.yml")
def user_update():
    return app_response(status.FORBIDDEN, message=UNSUPPORTED)


def main():
    app.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
