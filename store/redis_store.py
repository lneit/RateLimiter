"""A context manager for Redis store.
"""
from aioredis import create_redis


class RedisStore:
    """An asyncronous context manager for Redis Store.
    """

    def __init__(self, address, **kwargs):
        """Redis context manager constructor.
          Args:
            address: Redis host address
            kwargs: Other aioredis configuration parameters
        """
        self._address = address
        self._kwargs = kwargs
        self.store = None

    async def __aenter__(self):
        self.store = await create_redis(self._address, **self._kwargs)
        return self.store

    async def __aexit__(self, exc_type, exc, tb):
        self.store.close()
