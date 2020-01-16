FROM python:3.7.6-slim-buster

RUN apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y \
            gcc jq make automake libtool \
            build-essential curl wget && rm -rf /var/lib/apt/lists/* \
    && apt-get remove --auto-remove -y build-essential wget

# Copy requirements file
COPY ./requirements.txt /tmp/requirements.txt

# Install python modules
RUN pip3 install -r /tmp/requirements.txt \
    && mkdir -p /opt/app

COPY decorators /opt/app/decorators
COPY proxy /opt/app/proxy
COPY store /opt/app/store
COPY ./.env /opt/app/.env

ENV PYTHONPATH "/opt/app"

WORKDIR /opt/app

EXPOSE 7070

CMD ["hypercorn", "-b", "0.0.0.0:7070", "-w", "10", "proxy/app:PROXY"]
