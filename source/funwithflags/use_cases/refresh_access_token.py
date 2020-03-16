"""Module for refreshing access token implementation"""
from typing import Any

import flask_jwt_extended


def refresh_access_token(identity: Any) -> str:
    return flask_jwt_extended.create_access_token(identity=identity)
