#!/usr/bin/python3

# Copyright (C) 2023 Paul D. Gear
# License: AGPLv3

# Implementation of API endpoints:
# - data/ip_api -> get_station_data()
# - data/report -> save_station_measurements()

from datetime import datetime, timezone
import os
import time

from weather import data, influx, sun_times


default_latitude = float(os.environ['LATITUDE'])
default_longitude = float(os.environ['LONGITUDE'])
stations = {}
timestamps = {}


def get_station_data(rodata: dict) -> dict:
    """The Ecowitt station posts to this endpoint with the following variables set:
    - mac=MA:CA:DD:RE:SS:00
    - stationtype=EasyWeatherV1.5.2
    - fields=timezone,utc_offset,dst,date_sunrise,date_sunset
    This endpoint ignores the fields requested and hard codes all of the known data in the response.
    """
    # use cache data if it's less than 8 hours old
    if rodata['mac'] in stations and time.time() - timestamps[rodata['mac']] > 60 * 60 * 8.0:
        return stations[rodata['mac']]

    # otherwise refresh the data and keep it in cache
    data = {}
    data.update(sun_times.get_sun_times(default_latitude, default_longitude))
    timestamps[rodata['mac']] = time.time()
    stations[rodata['mac']] = data
    return data


def save_station_measurements(rodata: dict) -> None:
    """Perform standard conversions on the supplied weather data:
     - convert all field names to lower case
     - remove fields which should not be stored
     - convert values to metric SI units
     - rename fields to standardised readable names
    Then save to influxdb."""
    weather_data = {
        'date_received': datetime.now(timezone.utc),
    }
    weather_data.update(rodata)
    data.lower(weather_data)
    data.clean(weather_data)
    data.convert_numeric(weather_data)
    data.convert_date(weather_data)
    data.convert_metric(weather_data)
    data.rename(weather_data)
    influx.write(weather_data)
