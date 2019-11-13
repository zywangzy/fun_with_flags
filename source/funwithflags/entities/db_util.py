"""Utility module for database gateway."""
from configparser import ConfigParser
from typing import Mapping


def read_postgres_config(filename='database.ini', section='postgresql') -> Mapping[str, str]:
    """Read configuration file and return a dictionary mapping from field name to field value."""
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f"{filename} does not have section {section}, sections are {parser.sections()}")
    return db
