#!/usr/bin/python3

# Copyright (C) 2023 Paul D. Gear
# License: AGPLv3

# Retrieve sunrise & sunset times from api.sunrise-sunset.org and format them for
# the weather station. LATITUDE and LONGITUDE must be set in the environment.

import json
import os
import time
from datetime import datetime, timezone

import requests
import requests_cache

from . import influx

cachetime = 60 * 60 * 8

requests_cache.install_cache('sunrise_sunset_cache', backend='sqlite', expire_after=cachetime, use_temp=True)


# Cache local time zone name
time_zone_name = os.environ.get('TZ', None)
if time_zone_name is None:
    with open('/etc/timezone', 'r') as tzfile:
        time_zone_name = tzfile.readline().strip()


def get_sun_times(latitude, longitude, logger):
    r = requests.get(f'https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&formatted=0')
    data = json.loads(r.content)
    sunrise = datetime.fromisoformat(data['results']['sunrise']).astimezone()
    sunset = datetime.fromisoformat(data['results']['sunset']).astimezone()

    # FIXME: make this function just gather the data in canonical form
    # then the caller can write the results to influx and return them to the station

    # sunrise & sunset are recorded as seconds after the epoch to make them easy to convert to any date/time
    sun_data = {
        'date': datetime.now(timezone.utc),
        'dst': time.daylight,
        'sunrise': int(sunrise.timestamp()),
        'sunset': int(sunset.timestamp()),
        'timezone': time_zone_name,
        'utc_offset': -time.timezone,
    }
    logger.info(f"Saving sun: {sun_data}")
    influx.write('sun', sun_data)

    # the order of these fields is assumed to be significant - do not reorder
    results = {
        'timezone': time_zone_name,
        'utc_offset': str(-time.timezone),
        'dst': str(time.daylight),
        'date_sunrise': sunrise.strftime("%H:%M"),
        'date_sunset': sunset.strftime("%H:%M"),
    }
    return results
