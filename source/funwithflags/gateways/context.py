"""Definition of processing context."""
from dataclasses import dataclass

from .db_gateway import make_postgres_gateway, PostgresGateway


@dataclass
class Context:
    """The context class consists all the gateways and states necessary for service.
    """

    postgres_gateway: PostgresGateway

    def __init__(self, postgres_gateway=None):
        self.postgres_gateway = (
            make_postgres_gateway() if postgres_gateway is None else postgres_gateway
        )
