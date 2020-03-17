"""Module for Redis cache gateway."""
import logging

import redis

from funwithflags.entities import read_config_file


logger = logging.getLogger(__name__)


class RedisGateway:
    def __init__(self, host: str, port: int = 6379, db: int = 0):
        self._host = host
        self._port = port
        self._db = db
        self._redis = redis.Redis(host=self._host, port=self._port, db=self._db)

    def put(self, name: str, value: str) -> bool:
        return self._redis.set(name, value)

    def get(self, name: str) -> str:
        return self._redis.get(name)

    @staticmethod
    def create(filename="config.ini"):
        """Factory method to create a `RedisGateway` object.
        """
        try:
            section = "redis"
            config = read_config_file(filename, section)
            return RedisGateway()
        except KeyError as e:
            logger.error(f"Invalid config file \"{filename}\" section \"{section}\": {e}")
            raise e
        except Exception as e:
            logger.error(f"Failed to initialize RedisGateway: {e}")
            raise e
