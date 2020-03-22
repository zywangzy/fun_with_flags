"""Main entrypoint of RESTful API service."""
from http import HTTPStatus as status
import logging

from flask import Flask
from flask import jsonify, request, make_response
from flasgger import swag_from, Swagger
from flask_jwt_extended import get_raw_jwt, get_jwt_identity, JWTManager, jwt_refresh_token_required, jwt_required

from funwithflags.definitions import RegisterRequest, LoginRequest, LogoutRequest
from funwithflags.definitions import BadRequestError, DatabaseQueryError
from funwithflags.definitions import ACCESS_EXPIRES, REFRESH_EXPIRES
from funwithflags.gateways import Context
from funwithflags.use_cases import register, login, logout, refresh_access_token

logger = logging.getLogger(__name__)
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


@app.route("/api/user/<user_id>", methods=["GET"])
@swag_from("swagger_docs/user_read.yml")
def user_read(user_id):
    return app_response(status.FORBIDDEN, message=UNSUPPORTED)


@app.route("/api/user/register", methods=["POST"])
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


@app.route("/api/user/login", methods=["POST"])
@swag_from("swagger_docs/user_login.yml")
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
    except Exception as e:
        logger.info(
            f'An exception happened when handling login request "{content}": {e}'
        )
        return app_response(status.INTERNAL_SERVER_ERROR, message="Internal error")


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
    try:
        logout_request = LogoutRequest(jti)
        logout(logout_request, context)
        return app_response(status.OK, message="OK")
    except Exception as e:
        logger.info(f'An exception happened when handling logout request {logout_request}: {e}')
        return app_response(status.INTERNAL_SERVER_ERROR, message=f"Internal error")


@app.route("/api/user/update", methods=["POST"])
@swag_from("swagger_docs/user_update.yml")
def user_update():
    return app_response(status.FORBIDDEN, message=UNSUPPORTED)


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
