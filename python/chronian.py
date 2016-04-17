#!/usr/bin/python

# Chronian is a package for handling dates, times, and timezones.
# For details of the conceptual model on which it is based,
# see http://chronian.com.

# The MIT License (MIT)
#
# Copyright (c) 2016 Michael Scott Kenniston
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#       
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
# THE SOFTWARE.

from datetime import datetime
from pytz import timezone, all_timezones

JAN = 1
FEB = 2
MAR = 3
APR = 4
MAY = 5
JUN = 6
JUL = 7
AUG = 8
SEP = 9
OCT = 10
NOV = 11
DEC = 12

MON = 0
TUE = 1
WED = 2
THU = 3
FRI = 4
SAT = 5
SUN = 6

class ChronianError(Exception):
    pass


class InvalidOptionNameError(ChronianError):
    pass


class InvalidOptionValueError(ChronianError):
    pass


class NotImplementedError(ChronianError):
    pass


class MissingTimeZoneError(ChronianError):
    pass


class InvalidTimeZoneError(ChronianError):
    pass


# the first legal value is the default
VALID_OPTION_VALUES = {
    'date_system': ['Proleptic Gregorian calendar',
                    'Proleptic Julian calendar',
                   ],
    'leap_seconds': ['collapse leap seconds',
                     'smear leap seconds',
                     'UTC leap seconds',
                    ],
    'resolution': ['microsecond'],
    'time_system': ['modern 24-hour clock'],
    'time_zone_id': None,
    }

def validate_options(options):
    for key in options:
        if key not in VALID_OPTION_VALUES:
            raise InvalidOptionNameError('invalid option name "%s"' % key)
        value = options[key]
        legal_values = VALID_OPTION_VALUES[key]
        if legal_values and value not in legal_values:
            raise InvalidOptionValueError('invalid value "%s" for option "%s"' %
                    (value, key))

def validate_fields(fields):
    for bounds in [['month', 1, 12],
                   ['day_of_month', 1, 31],
                   ['hour', 0, 24],
                   ['minute', 0, 59],
                   ['second', 0, 60],
                   ['fraction', 0, 1000]]:
        (label, min, max) = bounds
        val = fields[label]
        if val < min or val > max:
            raise InvalidFieldValue('invalid field value "%s" for "%s"' %
                                (val, label))


class Chron:

    def __init__(self, options={}):
        validate_options(options)
        self._options = {}
        for key in VALID_OPTION_VALUES:
            values = VALID_OPTION_VALUES[key]
            self._options[key] = values[0] if values else None
        self._options.update(options)

    def options(self):
        return self._options.copy()

    def line(self, options={}):
        return ChronLine(self, options)


class ChronLine:
    def __init__(self, parent, options):
        validate_options(options)
        self._parent = parent
        self._options = parent.options()
        self._options.update(options)
        tzid = self._options['time_zone_id']
        if tzid is None:
            raise MissingTimeZoneError('time zone must be specified for ChronLine')
        if tzid not in all_timezones:
            raise InvalidTimeZoneError('invalid time zone "%s"' % tzid)
        self._time_zone = timezone(tzid)
        keys = self._options.keys()
        keys.sort()
        self._name = ", ".join([str(self._options[key]) for key in keys])

    def options(self):
        return self._options.copy()

    def name(self):
        return self._name

    def time_zone(self):
        return self._time_zone

    def point(self, year=1, month=1, day_of_month=1,
                    hour=0, minute=0, second=0, fraction=0):
        return ChronPoint().set_fields(self, year, month, day_of_month,
                                       hour, minute, second, fraction)


class ChronPoint:

    def __init__(self):
        pass

    def set_fields(self, parent, year, month, day_of_month, hour, minute, second, fraction):
        self._parent = parent
        self._internal = parent.time_zone().localize(datetime(year, month, day_of_month, hour, minute, second, fraction))
        return self

    def year(self):
        return self._internal.year

    def month(self):
        return self._internal.month

    def day_of_month(self):
        return self._internal.day

    def hour(self):
        return self._internal.hour

    def minute(self):
        return self._internal.minute

    def second(self):
        return self._internal.second

    def fraction(self):
        return self._internal.microsecond

    def day_of_week(self):
        return self._internal.weekday()

    def to(self, line):  # convert
        return self

    def through(self, last):  # make interval
        return [self, last]

    def to(self, line):  # convert
        other = ChronPoint()
        other._parent = line
        other_zone = other._parent.time_zone()
        other._internal = other_zone.normalize(self._internal.astimezone(other_zone))
        return other

    def format(self, spec=None):
        return str(self._internal)


class ChronClock:

    def __init__(self, line):
        self._line = line
        pass

    def read(line=None):
        if line is None:
            line = self._line
        return line.xfrom()
