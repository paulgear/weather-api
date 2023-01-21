#!/bin/sh

# Copyright (C) 2023 Paul D. Gear
# License: AGPLv3

# Wait for the InfluxDB token file to appear, then start the UWSGI
# application server with the token file's location in the environment.

cd /srv/weather-api

export INFLUXDB_TOKENFILE=/influxconfig/token.json
tries=1
while [ ! -f $INFLUXDB_TOKENFILE ]; do
    sleep $tries
    tries=$(expr $tries + 1)
    if [ $tries -gt 10 ]; then
        echo "Timed out waiting for influxdb token to appear in $INFLUXDB_TOKENFILE" >&2
        exit 1
    fi
done

uwsgi_python310 \
   --callable app \
   --disable-logging \
   --http-socket 0.0.0.0:8000 \
   --log-4xx \
   --log-5xx \
   --log-zero \
   --module app:app \
   --processes 2 \
   --threads 8 \
