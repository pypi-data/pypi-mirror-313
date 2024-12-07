import unittest

import ddt

from iker.common.utils.dtutils import dt_format, dt_format_iso, dt_parse, dt_parse_iso
from iker.common.utils.dtutils import dt_from_ts, dt_to_ts
from iker.common.utils.dtutils import dt_utc
from iker.common.utils.dtutils import dt_utc_epoch, dt_utc_max, dt_utc_min
from iker.common.utils.dtutils import iso_format


@ddt.ddt
class DtUtilsTest(unittest.TestCase):

    def test_dt_utc_min(self):
        self.assertEqual(dt_utc(1, 1, 1, 0, 0, 0, 0), dt_utc_min())
        self.assertEqual("0001-01-01T00:00:00.000000+0000", dt_format(dt_utc_min(), iso_format(True, True)))
        self.assertEqual("0001-01-01T00:00:00", dt_format_iso(dt_utc_min()))
        self.assertEqual(dt_parse_iso("0001-01-01T00:00:00.000000+0000"), dt_utc_min())
        self.assertEqual(dt_parse_iso("0001-01-01T00:00:00.000000"), dt_utc_min())

    def test_dt_utc_max(self):
        self.assertEqual(dt_utc(9999, 12, 31, 23, 59, 59, 999999), dt_utc_max())
        self.assertEqual("9999-12-31T23:59:59.999999+0000", dt_format(dt_utc_max(), iso_format(True, True)))
        self.assertEqual("9999-12-31T23:59:59", dt_format_iso(dt_utc_max()))
        self.assertEqual(dt_parse_iso("9999-12-31T23:59:59.999999+0000"), dt_utc_max())
        self.assertEqual(dt_parse_iso("9999-12-31T23:59:59.999999"), dt_utc_max())

    def test_dt_utc_epoch(self):
        self.assertEqual(dt_utc(1970, 1, 1, 0, 0, 0, 0), dt_utc_epoch())
        self.assertEqual(0.0, dt_to_ts(dt_utc_epoch()))
        self.assertEqual(dt_from_ts(0.0), dt_utc_epoch())
        self.assertEqual("1970-01-01T00:00:00.000000+0000", dt_format(dt_utc_epoch(), iso_format(True, True)))
        self.assertEqual("1970-01-01T00:00:00", dt_format_iso(dt_utc_epoch()))
        self.assertEqual(dt_parse_iso("1970-01-01T00:00:00.000000+0000"), dt_utc_epoch())
        self.assertEqual(dt_parse_iso("1970-01-01T00:00:00.000000"), dt_utc_epoch())

    @ddt.data(
        (dt_utc(1970, 1, 1), 0.0),
        (dt_utc(1969, 12, 31, 23, 59, 59), -1.0),
        (dt_utc(1970, 1, 1, 0, 0, 1), 1.0),
        (dt_utc(1970, 1, 1, 0, 0, 0, 1000), 0.001),
    )
    @ddt.unpack
    def test_dt_to_ts(self, data, expect):
        self.assertEqual(expect, dt_to_ts(data))

    @ddt.data(
        (0.0, dt_utc(1970, 1, 1)),
        (-1.0, dt_utc(1969, 12, 31, 23, 59, 59)),
        (1.0, dt_utc(1970, 1, 1, 0, 0, 1)),
        (0.001, dt_utc(1970, 1, 1, 0, 0, 0, 1000)),
    )
    @ddt.unpack
    def test_dt_to_from(self, data, expect):
        self.assertEqual(expect, dt_from_ts(data))

    @ddt.data(
        ("0001-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S", dt_utc(1, 1, 1, 0, 0, 0)),
        ("9999-12-31T23:59:59", "%Y-%m-%dT%H:%M:%S", dt_utc(9999, 12, 31, 23, 59, 59)),
        ("1970-01-01", "%Y-%m-%d", dt_utc(1970, 1, 1)),
        ("1970-01-01 12:30:45", "%Y-%m-%d %H:%M:%S", dt_utc(1970, 1, 1, 12, 30, 45)),
        ("1970-01-01T12:30:45", "%Y-%m-%dT%H:%M:%S", dt_utc(1970, 1, 1, 12, 30, 45)),
        ("1970-01-01T12:30:45", ["%H:%M:%S", "%Y-%m-%dT%H:%M:%S"], dt_utc(1970, 1, 1, 12, 30, 45)),
        ("1970-01-01T12:30:45", ("%H:%M:%S", "%Y-%m-%dT%H:%M:%S"), dt_utc(1970, 1, 1, 12, 30, 45)),
        ("2020-10-01", "%Y-%m-%d", dt_utc(2020, 10, 1)),
        ("2020-10-01 12:30:45", "%Y-%m-%d %H:%M:%S", dt_utc(2020, 10, 1, 12, 30, 45)),
        ("2020-10-01T12:30:45", "%Y-%m-%dT%H:%M:%S", dt_utc(2020, 10, 1, 12, 30, 45)),
        ("1949-10-01", "%Y-%m-%d", dt_utc(1949, 10, 1)),
        ("1949-10-01 12:30:45", "%Y-%m-%d %H:%M:%S", dt_utc(1949, 10, 1, 12, 30, 45)),
        ("1949-10-01T12:30:45", "%Y-%m-%dT%H:%M:%S", dt_utc(1949, 10, 1, 12, 30, 45)),

        ("0009-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S", dt_utc(9, 1, 1, 0, 0, 0)),
        ("0090-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S", dt_utc(90, 1, 1, 0, 0, 0)),
        ("0900-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S", dt_utc(900, 1, 1, 0, 0, 0)),
        ("9000-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S", dt_utc(9000, 1, 1, 0, 0, 0)),

        ("99-12-31/12:30:45", "%y-%m-%d/%H:%M:%S", dt_utc(1999, 12, 31, 12, 30, 45)),
        ("00-01-01/12:30:45", "%y-%m-%d/%H:%M:%S", dt_utc(2000, 1, 1, 12, 30, 45)),

        ("1999/99-12-31/12:30:45", "%Y/%y-%m-%d/%H:%M:%S", dt_utc(1999, 12, 31, 12, 30, 45)),
        ("2000/00-01-01/12:30:45", "%Y/%y-%m-%d/%H:%M:%S", dt_utc(2000, 1, 1, 12, 30, 45)),
        ("99/1999-12-31/12:30:45", "%y/%Y-%m-%d/%H:%M:%S", dt_utc(1999, 12, 31, 12, 30, 45)),
        ("00/2000-01-01/12:30:45", "%y/%Y-%m-%d/%H:%M:%S", dt_utc(2000, 1, 1, 12, 30, 45)),

        ("2999/99-12-31/12:30:45", "%Y/%y-%m-%d/%H:%M:%S", dt_utc(1999, 12, 31, 12, 30, 45)),
        ("1000/00-01-01/12:30:45", "%Y/%y-%m-%d/%H:%M:%S", dt_utc(2000, 1, 1, 12, 30, 45)),
        ("99/2999-12-31/12:30:45", "%y/%Y-%m-%d/%H:%M:%S", dt_utc(2999, 12, 31, 12, 30, 45)),
        ("00/1000-01-01/12:30:45", "%y/%Y-%m-%d/%H:%M:%S", dt_utc(1000, 1, 1, 12, 30, 45)),
    )
    @ddt.unpack
    def test_dt_parse(self, dt_str, fmt_str, expect):
        self.assertEqual(expect, dt_parse(dt_str, fmt_str))

    @ddt.data(
        (dt_utc(1, 1, 1, 0, 0, 0), "%Y-%m-%dT%H:%M:%S", "0001-01-01T00:00:00"),
        (dt_utc(9999, 12, 31, 23, 59, 59), "%Y-%m-%dT%H:%M:%S", "9999-12-31T23:59:59"),
        (dt_utc(1970, 1, 1), "%Y-%m-%d", "1970-01-01"),
        (dt_utc(1970, 1, 1, 12, 30, 45), "%Y-%m-%d %H:%M:%S", "1970-01-01 12:30:45"),
        (dt_utc(1970, 1, 1, 12, 30, 45), "%Y-%m-%dT%H:%M:%S", "1970-01-01T12:30:45"),
        (dt_utc(2020, 10, 1), "%Y-%m-%d", "2020-10-01"),
        (dt_utc(2020, 10, 1, 12, 30, 45), "%Y-%m-%d %H:%M:%S", "2020-10-01 12:30:45"),
        (dt_utc(2020, 10, 1, 12, 30, 45), "%Y-%m-%dT%H:%M:%S", "2020-10-01T12:30:45"),
        (dt_utc(1949, 10, 1), "%Y-%m-%d", "1949-10-01"),
        (dt_utc(1949, 10, 1, 12, 30, 45), "%Y-%m-%d %H:%M:%S", "1949-10-01 12:30:45"),
        (dt_utc(1949, 10, 1, 12, 30, 45), "%Y-%m-%dT%H:%M:%S", "1949-10-01T12:30:45"),

        (dt_utc(9, 1, 1, 0, 0, 0), "%Y-%m-%dT%H:%M:%S", "0009-01-01T00:00:00"),
        (dt_utc(90, 1, 1, 0, 0, 0), "%Y-%m-%dT%H:%M:%S", "0090-01-01T00:00:00"),
        (dt_utc(900, 1, 1, 0, 0, 0), "%Y-%m-%dT%H:%M:%S", "0900-01-01T00:00:00"),
        (dt_utc(9000, 1, 1, 0, 0, 0), "%Y-%m-%dT%H:%M:%S", "9000-01-01T00:00:00"),

        (dt_utc(1999, 12, 31, 12, 30, 45), "%y-%m-%d/%H:%M:%S", "99-12-31/12:30:45"),
        (dt_utc(2000, 1, 1, 12, 30, 45), "%y-%m-%d/%H:%M:%S", "00-01-01/12:30:45"),
        (dt_utc(1999, 12, 31, 12, 30, 45), "%Y/%y-%m-%d/%H:%M:%S", "1999/99-12-31/12:30:45"),
        (dt_utc(2000, 1, 1, 12, 30, 45), "%Y/%y-%m-%d/%H:%M:%S", "2000/00-01-01/12:30:45"),
        (dt_utc(1999, 12, 31, 12, 30, 45), "%y/%Y-%m-%d/%H:%M:%S", "99/1999-12-31/12:30:45"),
        (dt_utc(2000, 1, 1, 12, 30, 45), "%y/%Y-%m-%d/%H:%M:%S", "00/2000-01-01/12:30:45"),

        (dt_utc(9, 1, 1, 0, 0, 0), "%y-%m-%d/%H:%M:%S", "09-01-01/00:00:00"),
        (dt_utc(90, 1, 1, 0, 0, 0), "%y-%m-%d/%H:%M:%S", "90-01-01/00:00:00"),
        (dt_utc(900, 1, 1, 0, 0, 0), "%y-%m-%d/%H:%M:%S", "00-01-01/00:00:00"),
        (dt_utc(9000, 1, 1, 0, 0, 0), "%y-%m-%d/%H:%M:%S", "00-01-01/00:00:00"),
        (dt_utc(9, 1, 1, 0, 0, 0), "%Y/%y-%m-%d/%H:%M:%S", "0009/09-01-01/00:00:00"),
        (dt_utc(90, 1, 1, 0, 0, 0), "%Y/%y-%m-%d/%H:%M:%S", "0090/90-01-01/00:00:00"),
        (dt_utc(900, 1, 1, 0, 0, 0), "%Y/%y-%m-%d/%H:%M:%S", "0900/00-01-01/00:00:00"),
        (dt_utc(9000, 1, 1, 0, 0, 0), "%Y/%y-%m-%d/%H:%M:%S", "9000/00-01-01/00:00:00"),
    )
    @ddt.unpack
    def test_dt_format(self, dt, fmt_str, expect):
        self.assertEqual(expect, dt_format(dt, fmt_str))
