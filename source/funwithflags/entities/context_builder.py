"""Factory method to build processing context."""
from funwithflags.definitions import Context
from funwithflags.gateways import make_postgres_gateway


def make_context() -> Context:
    """Factory method to build Context object consisting PostgresGateway."""
    postgres_gateway = make_postgres_gateway()
    return Context(postgres_gateway)
