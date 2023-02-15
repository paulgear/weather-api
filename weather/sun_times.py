#!/usr/bin/python3

# Copyright (C) 2023 Paul D. Gear
# License: AGPLv3

# Retrieve sunrise & sunset times from api.sunrise-sunset.org and format them for
# the weather station. LATITUDE and LONGITUDE must be set in the environment.

from datetime import datetime
import json
import os
import time

import requests
import requests_cache

cachetime = 60 * 60 * 8

requests_cache.install_cache('sunrise_sunset_cache', backend='memory', expire_after=cachetime)


# Cache local time zone name
time_zone_name = os.environ.get('TZ', None)
if time_zone_name is None:
    with open('/etc/timezone', 'r') as tzfile:
        time_zone_name = tzfile.readline().strip()


# TODO: Record the results so we can show a chart of sunrise vs. sunset times over a year
def get_sun_times(latitude, longitude):
    r = requests.get(f'https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&formatted=0')
    data = json.loads(r.content)
    sunrise = datetime.fromisoformat(data['results']['sunrise']).astimezone()
    sunset = datetime.fromisoformat(data['results']['sunset']).astimezone()

    results = {
        'date_sunrise': sunrise.strftime("%H:%M"),
        'date_sunset': sunset.strftime("%H:%M"),
        'dst': str(time.daylight),
        'timezone': time_zone_name.replace('/', '\/'),
        'utc_offset': str(-time.timezone),
    }
    return results
