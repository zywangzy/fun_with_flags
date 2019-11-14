"""Utility module for database gateway."""
from configparser import ConfigParser
from typing import List, Mapping


def read_postgres_config(
    filename="database.ini", section="postgresql"
) -> Mapping[str, str]:
    """Read configuration file and return a dictionary mapping from field name to field value."""
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            f"{filename} does not have section {section}, sections are {parser.sections()}"
        )
    return db


def generate_update_params(uid, **kwargs) -> (str, List):
    """Helper function to generate a string of multiple field assignment and a list of values to
    be assigned.
    """
    valid_fields = {"username", "nickname", "password", "email"}
    field_values = [(key, val) for key, val in kwargs.items() if key in valid_fields]
    return (
        ", ".join([key + " = %s" for key, _ in field_values]),
        tuple([val for _, val in field_values] + [uid] if field_values else []),
    )
