#!/bin/sh

# Copyright (C) 2023 Paul D. Gear
# License: AGPLv3

# Create an InfluxDB auth token and save it in $OUTFILE for use by the weather API.
# This script should be located in /docker-entrypoint-initdb.d for the InfluxDB docker
# image to pick up and run, and /etc/influxdb2 should be mapped into the weather
# container for the weather API to use.

OUTFILE=/etc/influxdb2/token.json
if [ ! -f $OUTFILE ]; then
    influx auth create --write-buckets --json > $OUTFILE
    chmod 644 $OUTFILE
fi
