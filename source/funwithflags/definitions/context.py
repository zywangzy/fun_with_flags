"""Definition of processing context."""
from dataclasses import dataclass

from funwithflags.gateways import PostgresGateway


@dataclass
class Context:
    postgres_gateway: PostgresGateway
