"""Rate limit decorator. Designed to work in a quart/flask application context.
Uses Redis store to keep the track of the number of requests per interval.
By default, uses the Remote-Addr header of the request as a key in Redis store.
Reads Redis HOST name and a Requestor identity field from the REDIS_HOST and REQUEST_HEADER
environment variables respectively.
"""
import functools
import os
from http import HTTPStatus
from quart import request
from store.redis_store import RedisStore


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REQUEST_HEADER = os.getenv("REQUEST_HEADER", "Remote-Addr")


def rate_limit(count, interval):
    """Rate limit decorator.
    Args:
      count (int):    A max number of requests to allow per interval.
      interval (int): A period of time in seconds.
    Returns:
      A rate limiting wrapper for the original function.
  """

    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args):
            async with RedisStore(REDIS_HOST) as store:
                key = request.headers[REQUEST_HEADER]
                current_count = await store.get(key)
                if not current_count:
                    # There is no such key entry in the store yet. Set the key and its TTL
                    await store.set(key, 1, expire=interval)
                elif int(current_count) >= count:
                    # Reject the request as the rate limit has been exceeded
                    return (
                        {"message": "Rate limit exceeded. Please try again later."},
                        HTTPStatus.TOO_MANY_REQUESTS,
                    )
                else:
                    # Increment the counter
                    await store.incr(key)

                return await func(*args)

        return wrapped

    return wrapper
