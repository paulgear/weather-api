#!/usr/bin/python3

# Copyright (C) 2023 Paul D. Gear
# License: AGPLv3

# Implementation of weather data conversion methods.

from datetime import datetime, timezone

from weather import units


date_fields = {
    "dateutc",
}

ignored_fields = {
    "passkey",
    "password",
}

numeric_fields = {
    "absbaromin",
    "baromabsin",
    "baromin",
    "baromrelin",
    "dailyrainin",
    "dewptf",
    "eventrainin",
    "humidity",
    "humidityin",
    "indoorhumidity",
    "indoortempf",
    "monthlyrainin",
    "rainin",
    "rainratein",
    "realtime",
    "rtfreq",
    "solarradiation",
    "tempf",
    "tempinf",
    "totalrainin",
    "uv",
    "weeklyrainin",
    "wh65batt",
    "windchillf",
    "winddir",
    "windgustmph",
    "windspeedmph",
    "yearlyrainin",
}

rename_fields = {
    "absbaromin": "barometer_absolute",
    "baromabsin": "barometer_absolute",
    "baromin": "barometer",
    "baromrelin": "barometer",
    "dailyrainin": "rain_daily",
    "dateutc": "date",
    "dewptf": "dew_point",
    "eventrainin": "rain_event",
    "freq": "frequency",
    "humidityin": "humidity_indoor",
    "indoorhumidity": "humidity_indoor",
    "indoortempf": "temperature_indoor",
    "model": "hardware",
    "monthlyrainin": "rain_monthly",
    "rainin": "rain_hourly",
    "rainratein": "rain_rate",
    "rtfreq": "realtime_freq",
    "softwaretype": "software",
    "solarradiation": "solar_radiation",
    "stationtype": "software",
    "tempf": "temperature",
    "tempinf": "temperature_indoor",
    "totalrainin": "rain_total",
    "weeklyrainin": "rain_weekly",
    "wh65batt": "battery",
    "windchillf": "wind_chill",
    "winddir": "wind_direction",
    "windgustmph": "wind_speed_gust",
    "windspeedmph": "wind_speed",
    "yearlyrainin": "rain_yearly",
}


def clean(data: dict) -> None:
    """Remove all of the fields we don't want to write to the data store"""
    for key in ignored_fields:
        if key in data:
            del data[key]


def convert_date(data: dict) -> None:
    """Convert the date string to a date object, in UTC"""
    for key in date_fields:
        if key in data:
            data[key] = datetime.fromisoformat(data[key]).replace(tzinfo=timezone.utc)


def convert_metric(data: dict) -> None:
    """Convert all data to metric"""

    # temperature requires a different conversion
    for key in units.temperature_fields:
        if key in data:
            data[key] = units.convert_temperature(data[key])

    # all the rest can be just looked up and coverted automatically
    for key in units.convert_fields:
        if key in data:
            data[key] = units.convert_measurement(key, data[key])


def convert_numeric(data: dict) -> None:
    """Convert numeric fields to floats"""
    for key in numeric_fields:
        if key in data:
            data[key] = float(data[key])


def lower(data: dict) -> None:
    """Convert all uppercase keys to lower case"""
    to_convert = [x for x in data if x != x.lower()]
    for key in to_convert:
        data[key.lower()] = data[key]
        del data[key]


def rename(data: dict) -> None:
    """Rename all fields to standardised, comprehensible names"""
    for key in rename_fields:
        if key in data:
            data[rename_fields[key]] = data[key]
            del data[key]
