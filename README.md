# RateLimiter
HTTP Request rate limiting proxy microservice.

__Run rl-proxy Locally__

**Pre-requisites
Run redis as a demon and set the REDIS_HOST environment variable
```
pipenv install
pipenv shell
source .env
export $(cut -d= -f1 ../.env)
quart run
```

To send a request:
```
curl -X GET http://localhost:5000
```

__Environment Variables__
```
QUART_APP=proxy/app:proxy
REDIS_HOST=redis://localhost
REQUEST_HEADER=Remote-Addr
REQUEST_COUNT=100
INTERVAL=3600
```

__Dependencies__
Redis has to be run locally for testapp command or the local run

__Integration Test__
pipenv run testapp

__Unit Test__
pipenv run unittest

__Open API Generation__
pipenv run openapi

__Deployment Automation__
Work in progress
