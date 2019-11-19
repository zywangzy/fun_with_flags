"""Definition of processing context."""
from dataclasses import dataclass

from .db_gateway import make_postgres_gateway, PostgresGateway


@dataclass
class Context:
    postgres_gateway: PostgresGateway


def make_context(postgres_gateway=None) -> Context:
    """Factory method to build Context object consisting PostgresGateway."""
    if postgres_gateway is None:
        postgres_gateway = make_postgres_gateway()
    return Context(postgres_gateway)
