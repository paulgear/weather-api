
# Copyright (C) 2023 Paul D. Gear
# License: AGPLv3

FROM paulgear/base:latest

ARG     PKGS="\
python3-flask \
python3-pint \
python3-pip \
python3-requests \
python3-requests-cache \
uwsgi \
uwsgi-plugin-python3 \
"
ENV     DEBIAN_FRONTEND=noninteractive

RUN     apt update && \
        apt install --no-install-recommends -y ${PKGS} && \
        rm -rf /var/lib/apt/lists/*

WORKDIR /srv/weather-api

COPY    *.txt .
RUN     pip3 install --no-cache-dir -r requirements.txt

COPY    app/*.py app/
COPY    weather/*.py weather/
COPY    influxsetup/* influxsetup/

COPY    entrypoint.sh .
RUN     chmod 0755 entrypoint.sh

RUN     adduser --disabled-password --gecos '' --home /srv/weather-api weather
USER    weather

EXPOSE  8000

ENTRYPOINT ["/srv/weather-api/entrypoint.sh"]
