#!/usr/bin/python3

# Copyright (C) 2023 Paul D. Gear
# License: AGPLv3

# Write weather data to InfluxDB via the API client. The variables
# INFLUXDB_BUCKET, INFLUXDB_ORG, INFLUXDB_TOKENFILE, and INFLUXDB_URL
# must be present in the environment.

import datetime
import json
import os

from influxdb_client import InfluxDBClient, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Retrieve InfluxDB connectivity information from the environment
# and the auth token from the token file.
influxdb_bucket = os.environ['INFLUXDB_BUCKET']
influxdb_org = os.environ['INFLUXDB_ORG']
influxdb_tokenfile = os.environ['INFLUXDB_TOKENFILE']
influxdb_url = os.environ['INFLUXDB_URL']

with open(influxdb_tokenfile, 'r') as f:
    json_data = json.load(f)
    influxdb_token = json_data['token']

# Intialise the InfluxDB client
influxdb_client = InfluxDBClient(
    org=influxdb_org,
    token=influxdb_token,
    url=influxdb_url,
)
write_client = influxdb_client.write_api(write_options=SYNCHRONOUS)


def extract_fields(data: dict) -> dict:
    """Return a dict containing only floating point and datetime values from the source data"""
    floats = {x: data[x] for x in data if type(data[x]) is float}
    dates = {x: data[x].timestamp() for x in data if type(data[x]) is datetime.datetime}
    floats.update(dates)
    return floats


def extract_tags(data: dict) -> dict:
    """Return a dict containing only string values from the source data"""
    fields = {x: data[x] for x in data if type(data[x]) is str}
    return fields


def write(measurement: str, data: dict) -> None:
    """Write the data to InfluxDB at second (coarsest) precision, supplying the tags and numeric fields"""
    timestamp = int(data['date'].timestamp())
    del data['date']

    fields = extract_fields(data)
    tags = extract_tags(data)
    # TODO: Add check for unknown fields
    write_client.write(influxdb_bucket, influxdb_org, {
        'fields': fields,
        'measurement': measurement,
        'tags': tags,
        'time': timestamp,
    }, write_precision=WritePrecision.S)
