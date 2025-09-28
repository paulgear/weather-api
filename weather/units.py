#!/usr/bin/python3

# Copyright (C) 2023 Paul D. Gear
# License: AGPLv3

# Implementation of metric conversion methods using pint https://pint.readthedocs.io/

import pint

reg = pint.UnitRegistry()


convert_fields = {
    "dailyrainin": (reg.inch, "meter"),
    "eventrainin": (reg.inch, "meter"),
    "monthlyrainin": (reg.inch, "meter"),
    "rainin": (reg.inch, "meter"),
    "totalrainin": (reg.inch, "meter"),
    "weeklyrainin": (reg.inch, "meter"),
    "yearlyrainin": (reg.inch, "meter"),
    "absbaromin": (reg.inHg, "pascal"),
    "baromabsin": (reg.inHg, "pascal"),
    "baromin": (reg.inHg, "pascal"),
    "baromrelin": (reg.inHg, "pascal"),
    "rainratein": (reg.inch / reg.hour, "meter / hour"),
    "windspeedmph": (reg.mph, "kph"),
    "windgustmph": (reg.mph, "kph"),
}

temperature_fields = [
    "dewptf",
    "indoortempf",
    "tempf",
    "tempinf",
    "windchillf",
]


def convert_measurement(name: str, val: float) -> float:
    """convert multiplicative units"""
    measurement = val * convert_fields[name][0]
    return measurement.m_as(convert_fields[name][1])


def convert_temperature(t: float) -> float:
    """convert Fahrenheit to Celsius"""
    fahrenheit = reg.Quantity(t, reg.degF)
    return fahrenheit.m_as("degC")
