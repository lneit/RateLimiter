HTTP Request rate limiting proxy microservice.

__Environment Variables__
```
QUART_APP=proxy/app:proxy
REDIS_HOST=redis://localhost
REQUEST_HEADER=Remote-Addr
REQUEST_COUNT=100
INTERVAL=3600
```

__Dependencies__
Redis has to be run locally for testapp command

__Integration Test__
pipenv run testapp

__Unit Test__
pipenv run unittest

__Open API Generation__
pipenv run openapi

__Deployment Automation__
Work in progress# RateLimiter
