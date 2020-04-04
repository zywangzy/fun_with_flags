"""Main entrypoint of RESTful API service."""
from http import HTTPStatus as status
import logging

from flask import Flask
from flask import jsonify, request, make_response
from flasgger import swag_from, Swagger
from flask_jwt_extended import (
    fresh_jwt_required,
    get_raw_jwt,
    get_jwt_identity,
    JWTManager,
    jwt_refresh_token_required,
    jwt_required
)

from funwithflags.definitions import (RegisterRequest, LoginRequest, LogoutRequest, FreshLoginRequest,
                                      UserUpdateRequest)
from funwithflags.definitions import BadRequestError, DatabaseQueryError
from funwithflags.definitions import ACCESS_EXPIRES, REFRESH_EXPIRES
from funwithflags.entities.logging_util import get_module_logger
from funwithflags.gateways import Context
from funwithflags.use_cases import (register, login, fresh_login, logout, read_user_basic, refresh_access_token,
                                    update_user)

logger = get_module_logger(__name__)
context = Context()
app = Flask(__name__)

# Setup the jwt relevant config
app.config['JWT_SECRET_KEY'] = 'super-secret'  # TODO: Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = REFRESH_EXPIRES
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['refresh']  # Only check refresh token
jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    """Return true if decrypted_token is revoked."""
    jti = decrypted_token['jti']
    value = context.redis_gateway.get(jti)
    return value is None or value == "logout"


# Setup Swagger config
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

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/api/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/api/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/apidocs/"
}

swagger = Swagger(app, config=swagger_config)


UNSUPPORTED = "Unsupported function"


def app_response(code, message, **data):
    """Helper function of Flask to return json response. Will return a json object with structure of
    {"code": code, "msg": message, "data": data}, e.g. {"code": 200, "msg": "OK", "data": 1}.
    """
    return make_response(jsonify(message=message, **data), code)


def handle_internal_error(func):
    """ Define the decorator for Flask API functions to log unhandled exceptions.
    """
    def error_handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.info(f'An exception happened when handling {func.__name__} request: {e}')
            return app_response(status.INTERNAL_SERVER_ERROR, message="Internal error")
    error_handler.__name__ = func.__name__
    return error_handler


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/api/user/user/<user_id>", methods=["GET"])
@jwt_required
@swag_from("swagger_docs/user_read.yml")
@handle_internal_error
def user_read(user_id):
    try:
        user = read_user_basic(int(user_id), context)
        return app_response(status.OK, message="OK", **user)
    except ValueError:
        return app_response(status.BAD_REQUEST, message="Invalid user id")
    except BadRequestError as e:
        return app_response(status.NOT_FOUND, message="User not found")
    except DatabaseQueryError as e:
        return app_response(status.NOT_FOUND, message="Read user error")


@app.route("/api/user/register", methods=["POST"])
@swag_from("swagger_docs/user_register.yml")
@handle_internal_error
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


@app.route("/api/user/login", methods=["POST"])
@swag_from("swagger_docs/user_login.yml")
@handle_internal_error
def user_login():
    try:
        content = request.get_json(force=True)
        login_request = LoginRequest(username=content["username"], password=content["password"])
        username, access_token, refresh_token = login(login_request, context)
        return app_response(
            status.OK,
            message="OK",
            username=username,
            access_token=access_token,
            refresh_token=refresh_token)
    except (KeyError, BadRequestError):
        return app_response(status.BAD_REQUEST, message="Invalid request")
    except DatabaseQueryError:
        return app_response(status.NOT_FOUND, message="Username not found")


@app.route("/api/user/fresh_login", methods=["POST"])
@jwt_refresh_token_required
@swag_from("swagger_docs/user_fresh_login.yml")
def user_fresh_login():
    try:
        content = request.get_json(force=True)
        login_request = FreshLoginRequest(user_id=get_jwt_identity(), password=content["password"])
        fresh_access_token = fresh_login(login_request, context)
        return app_response(status.OK, message="OK", access_token=fresh_access_token)
    except (KeyError, BadRequestError):
        return app_response(status.BAD_REQUEST, message="Invalid request")
    except DatabaseQueryError:
        return app_response(status.NOT_FOUND, message="User not found")


@app.route("/api/user/refresh_access_token", methods=["POST"])
@jwt_refresh_token_required
@swag_from("swagger_docs/user_refresh.yml")
def user_refresh_access_token():
    user_id = get_jwt_identity()
    if not user_id:
        return app_response(status.UNAUTHORIZED, message="Unauthorized error: invalid refresh token")
    access_token = refresh_access_token(identity=user_id, context=context)
    return app_response(status.CREATED, message="Created", access_token=access_token)


@app.route("/api/user/logout", methods=["DELETE"])
@jwt_refresh_token_required
@swag_from("swagger_docs/user_logout.yml")
def user_logout():
    jti = get_raw_jwt().get('jti', None)
    user_id = get_jwt_identity()
    if not jti or not user_id:
        return app_response(status.UNAUTHORIZED, message="Unauthorized error")
    logout_request = LogoutRequest(jti)
    logout(logout_request, context)
    return app_response(status.OK, message="OK")


@app.route("/api/user/update", methods=["POST"])
@jwt_required
@swag_from("swagger_docs/user_update.yml")
def user_update():
    try:
        user_id = get_jwt_identity()
        content = request.get_json(force=True)
        update_request = UserUpdateRequest(user_id=user_id, fields={k: v for k, v in content.items()})
        update_user(update_request, context)
        return app_response(status.OK, message="Updated")
    except BadRequestError as e:
        return app_response(status.BAD_REQUEST, message=f"Bad request: {e}")


@app.route("/api/user/update_protected", methods=["POST"])
@fresh_jwt_required
@swag_from("swagger_docs/user_update.yml")
def user_update_secret():
    try:
        user_id = get_jwt_identity()
        content = request.get_json(force=True)
        update_request = UserUpdateRequest(user_id=user_id, fields={k: v for k, v in content.items()}, protected=True)
        update_user(update_request, context)
        return app_response(status.OK, message="Updated")
    except BadRequestError as e:
        return app_response(status.BAD_REQUEST, message=f"Bad request: {e}")
    except DatabaseQueryError:
        return app_response(status.UNAUTHORIZED, "Unauthorized error: user not found")


@app.route("/api/project/<project_id>", methods=["GET"])
@swag_from("swagger_docs/project_read.yml")
def project_read(project_id):
    return app_response(status.FORBIDDEN, message=UNSUPPORTED)


@app.route("/api/project/create", methods=["POST"])
@swag_from("swagger_docs/project_create.yml")
def project_create():
    return app_response(status.FORBIDDEN, message=UNSUPPORTED)


def main():
    app.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
