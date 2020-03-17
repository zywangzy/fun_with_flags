"""Definition of processing context."""
from dataclasses import dataclass
from typing import Optional

from .db_gateway import PostgresGateway
from .redis_gateway import RedisGateway


@dataclass
class Context:
    """The context class consists all the gateways and states necessary for service.
    """

    postgres_gateway: PostgresGateway
    redis_gateway: RedisGateway

    def __init__(self, postgres_gateway: Optional[PostgresGateway] = None, redis_gateway: Optional[RedisGateway] = None):
        self.postgres_gateway = postgres_gateway if postgres_gateway else PostgresGateway.create()
        self.redis_gateway = redis_gateway if redis_gateway else RedisGateway.create()
