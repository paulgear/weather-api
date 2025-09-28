#!/usr/bin/python3

# Copyright (C) 2023 Paul D. Gear
# License: AGPLv3

# Implementation of API endpoints:
# - data/ip_api -> get_station_data()
# - data/report -> save_station_measurements()

import os
from datetime import datetime, timezone

from . import data, influx, sun_times

default_latitude = float(os.environ["LATITUDE"])
default_longitude = float(os.environ["LONGITUDE"])
stations = {}
timestamps = {}


def get_station_data(rodata: dict, logger: object) -> dict:
    """The Ecowitt station posts to this endpoint with the following variables set:
    - mac=MA:CA:DD:RE:SS:00
    - stationtype=EasyWeatherV1.5.2
    - fields=timezone,utc_offset,dst,date_sunrise,date_sunset
    This endpoint ignores the fields requested and hard codes the data in the response.
    """
    return sun_times.get_sun_times(default_latitude, default_longitude, logger=logger)


def save_station_measurements(rodata: dict) -> None:
    """Perform standard conversions on the supplied weather data:
     - convert all field names to lower case
     - remove fields which should not be stored
     - convert values to metric SI units
     - rename fields to standardised readable names
    Then save to influxdb."""
    weather_data = {
        "date_received": datetime.now(timezone.utc),
    }
    weather_data.update(rodata)
    data.lower(weather_data)
    data.clean(weather_data)
    data.convert_numeric(weather_data)
    data.convert_date(weather_data)
    data.convert_metric(weather_data)
    data.rename(weather_data)
    influx.write("weather", weather_data)
