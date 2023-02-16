#!/usr/bin/python3

# Copyright (C) 2023 Paul D. Gear
# License: AGPLv3

# Application routes for the Weather API

import json
import pprint
import time

from flask import request

from app import app
import weather


# This is useful as a liveness check or for returning something
# to management systems which auto-probe services.
@app.route('/')
def ok():
    return 'OK'


@app.route('/data/ip_api/', methods=['POST'])
def ecowitt_sun_data():
    sun_data = weather.get_station_data(request.form, logger=app.logger)
    result = json.dumps(sun_data, separators=(',', ':')).replace('/', '\/')
    app.logger.warning(f"ecowitt_sun_data: result={result}")
    return result


# References:
# https://github.com/iz0qwm/ecowitt_http_gateway/blob/master/index.php
@app.route('/data/report/', methods=['POST'])
def ecowitt_weather_data():
    if 'dateutc' not in request.form:
        # it's probably a sunrise/sunset request instead
        return ecowitt_sun_data()

    weather.save_station_measurements(request.form)
    return json.dumps({
        'errcode': 0,
        'errmsg': 'ok',
        # Eventually, this should look up the timezone offset for the station in a database;
        # for now, it's just assumed to be in the same timezone as the server.  The python
        # time.timezone object is expressed in offset to UTC from local rather than offset
        # from UTC to local, so needs to be sign-reversed for the weather station.
        'UTC_offset': -time.timezone,
    })


# References:
# https://support.weather.com/s/article/PWS-Upload-Protocol?language=en_US
# https://github.com/ccgruber/updateweatherstation/blob/master/pws_protocol.txt
# https://github.com/ccgruber/updateweatherstation/blob/master/updateweatherstation.php
# https://github.com/WinSCaP/wunderground2mqtt/blob/master/updateweatherstation.php
@app.route('/weatherstation/updateweatherstation.php')
def wunderground():
    weather.save_station_measurements(request.args)
    return 'success'
