"""Module for Redis cache gateway."""
from datetime import timedelta
import logging
from typing import Optional

import redis

from funwithflags.entities import read_config_file


logger = logging.getLogger(__name__)


class RedisGateway:
    def __init__(self, host: str, port: int = 6379, db: int = 0):
        self._host = host
        self._port = port
        self._db = db
        self._redis = redis.Redis(host=self._host, port=self._port, db=self._db)

    def set(self, name: str, value: str, expire: Optional[timedelta] = None) -> bool:
        return self._redis.set(name, value, ex=expire)

    def get(self, name: str) -> Optional[str]:
        value = self._redis.get(name)
        return value.decode("utf-8") if value else value

    @staticmethod
    def create(filename="config.ini"):
        """Factory method to create a `RedisGateway` object.
        """
        try:
            section = "redis"
            config = read_config_file(filename, section)
            return RedisGateway(host=config["host"], port=int(config["port"]), db=int(config["db"]))
        except KeyError as e:
            logger.error(f"Invalid config file \"{filename}\" section \"{section}\": {e}")
            raise e
        except Exception as e:
            logger.error(f"Failed to initialize RedisGateway: {e}")
            raise e
