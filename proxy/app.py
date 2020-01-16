"""A Quart application module for the rate limiting proxy solution.
Uses REQUEST_COUNT and INTERVAL environment variables to configure the rate for
a root ("/") endpoint.
Replies Hello! to all valid requests. Rejects all rate exceeding requests with
429 statius code.
"""
import os
from quart import Quart, redirect, url_for
from quart_openapi import Pint, Resource
from decorators.rate_limit import rate_limit


REQUEST_COUNT = os.getenv("REQUEST_COUNT", "1")
INTERVAL = os.getenv("INTERVAL", "5")

PROXY = Pint(__name__, title="Rate Limiting Proxy App")


@PROXY.route("/")
class RateLimitProxyRoot(Resource):
    """This route is used to limit the rate of the incoming requests to a
    configured REQUEST_COUNT per INTERVAL. The configuration is read from
    the environment.
    """
    @rate_limit(int(REQUEST_COUNT), int(INTERVAL))
    async def get(self):
        """Get request.
        """
        return "Hello!"


if __name__ == "__main__":
    PROXY.run(port=7070)
