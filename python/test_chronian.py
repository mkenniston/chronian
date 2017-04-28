#!/usr/bin/python

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
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import unittest
from chronian import \
    Chron, ChronClock, InvalidOptionNameError, InvalidOptionValueError, \
    MissingTimeZoneError


class ChronTest(unittest.TestCase):

    def testChronCtorNoOptions(self):
        options = Chron().options()
        self.assertEqual('Proleptic Gregorian calendar',
                         options['date_system'])
        self.assertEqual('collapse leap seconds',
                         options['leap_seconds'])
        self.assertEqual('microsecond',
                         options['resolution'])
        self.assertEqual('modern 24-hour clock',
                         options['time_system'])
        self.assertEqual(None,
                         options['time_zone_id'])

    def testChronCtorWithOptions(self):
        chron = Chron({'leap_seconds': 'UTC leap seconds'})
        self.assertEqual('modern 24-hour clock',
                         chron.options()['time_system'])
        self.assertEqual('UTC leap seconds',
                         chron.options()['leap_seconds'])

    def testInvalidOptionName(self):
        self.assertRaises(
            InvalidOptionNameError, Chron, {'cat': 'dog'})

    def testInvalidOptionValue(self):
        self.assertRaises(
            InvalidOptionValueError, Chron, {'leap_seconds': 'pig'})


class ChronLineTest(unittest.TestCase):

    def setUp(self):
        self.chron = Chron({'leap_seconds': 'UTC leap seconds'})
        self.chron_with_zone = Chron({'leap_seconds': 'UTC leap seconds',
                                      'time_zone_id': 'US/Central'})

    def testLineCtorNoArgsNoZone(self):
        self.assertRaises(MissingTimeZoneError, self.chron.line)

    def testLineCtorNoArgsWithZone(self):
        line = self.chron_with_zone.line()
        self.assertEqual('US/Central',
                         line.options()['time_zone_id'])

    def testLineCtorWithArgsNoZone(self):
        self.assertRaises(MissingTimeZoneError,
                          self.chron.line,
                          {'leap_seconds': 'collapse leap seconds'})

    def testLineCtorWithArgsWithZone(self):
        line = self.chron.line({'date_system': 'Proleptic Julian calendar',
                                'time_zone_id': 'US/Mountain'})
        options = line.options()
        self.assertEqual('Proleptic Julian calendar',
                         options['date_system'])
        self.assertEqual('UTC leap seconds',
                         options['leap_seconds'])
        self.assertEqual('modern 24-hour clock',
                         options['time_system'])
        self.assertEqual('US/Mountain',
                         options['time_zone_id'])

    def testLineName(self):
        expected = 'Proleptic Gregorian calendar, UTC leap seconds, ' \
            'microsecond, modern 24-hour clock, US/Central'
        self.assertEqual(expected,
                         self.chron_with_zone.line().name())


class ChronPointTest(unittest.TestCase):

    def setUp(self):
        self.line = Chron().line({'time_zone_id': 'UTC'})

    def testPointCtorNoArgs(self):
        p = self.line.point()
        self.assertEqual(1, p.year())
        self.assertEqual(0, p.fraction())

    def testPointCtorHeadArgs(self):
        p = self.line.point(1957, 1, 3, 22)
        self.assertEqual(1957, p.year())
        self.assertEqual(Chron.JAN, p.month())
        self.assertEqual(3, p.day_of_month())
        self.assertEqual(22, p.hour())
        self.assertEqual(0, p.minute())
        self.assertEqual(0, p.second())
        self.assertEqual(0, p.fraction())
        self.assertEqual(Chron.THU, p.day_of_week())

    def testPointCtorTailArgs(self):
        p = self.line.point(1957, minute=23, second=45, fraction=789)
        self.assertEqual(1957, p.year())
        self.assertEqual(23, p.minute())
        self.assertEqual(45, p.second())
        self.assertEqual(789, p.fraction())
        self.assertEqual(Chron.TUE, p.day_of_week())

    def testPointFormatNoArg(self):
        p = self.line.point(1969, 7, 20, 20, 18)
        self.assertEqual('1969-07-20 20:18:00+00:00', p.format())

    def testPointTo(self):
        p = self.line.point(1969, 7, 20, 20, 18)
        ET = Chron().line({'time_zone_id': 'America/New_York'})
        PT = Chron().line({'time_zone_id': 'US/Pacific'})
        self.assertEqual('1969-07-20 20:18:00+00:00', p.format())
        self.assertEqual('1969-07-20 16:18:00-04:00', p.to(ET).format())
        self.assertEqual('1969-07-20 13:18:00-07:00', p.to(PT).format())


class ChronClockTest(unittest.TestCase):

    def setUp(self):
        self.clock = ChronClock('line')


if __name__ == '__main__':
    unittest.main()
