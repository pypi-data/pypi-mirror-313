import datetime

from iker.common.utils.funcutils import memorized, singleton

__all__ = [
    "iso_dt_format",
    "iso_tm_format",
    "iso_format",
    "iso_formats",
    "dt_utc_min",
    "dt_utc_max",
    "dt_utc_epoch",
    "dt_utc_infinity",
    "dt_utc_now",
    "dt_utc",
    "dt_to_ts",
    "dt_from_ts",
    "dt_parse",
    "dt_format",
    "dt_parse_iso",
    "dt_format_iso",
]


@singleton
def iso_dt_format() -> str:
    return "%Y-%m-%d"


@singleton
def iso_tm_format() -> str:
    return "%H:%M:%S"


@memorized
def iso_format(with_ms: bool = False, with_tz: bool = False) -> str:
    fmt_str = "%Y-%m-%dT%H:%M:%S"
    if with_ms:
        fmt_str = fmt_str + ".%f"
    if with_tz:
        fmt_str = fmt_str + "%z"
    return fmt_str


@singleton
def iso_formats() -> list[str]:
    return [
        iso_format(),
        iso_format(True, False),
        iso_format(False, True),
        iso_format(True, True),
        iso_dt_format(),
        iso_tm_format(),
    ]


@singleton
def dt_utc_min() -> datetime.datetime:
    return datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)


@singleton
def dt_utc_max() -> datetime.datetime:
    return datetime.datetime.max.replace(tzinfo=datetime.timezone.utc)


@singleton
def dt_utc_epoch() -> datetime.datetime:
    return datetime.datetime(1970, 1, 1, 0, 0, 0, 0, tzinfo=datetime.timezone.utc)


dt_utc_infinity = dt_utc_max


def dt_utc_now() -> datetime.datetime:
    """
    Returns instance of current date time in UTC

    :return: current date time in UTC
    """
    return datetime.datetime.now(tz=datetime.timezone.utc)


def dt_utc(
    year: int,
    month: int = None,
    day: int = None,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
    microsecond: int = 0
) -> datetime.datetime:
    """
    Returns instance of the specified date time in UTC

    :param year: year part
    :param month: month part
    :param day: day part
    :param hour: hour part
    :param minute: minute part
    :param second: second part
    :param microsecond: microsecond part

    :return: specified date time in UTC
    """
    return datetime.datetime(year, month, day, hour, minute, second, microsecond, tzinfo=datetime.timezone.utc)


def dt_to_ts(dt: datetime.datetime) -> float:
    """
    Returns corresponding timestamp in seconds of the given datetime

    :param dt: the given datetime

    :return: timestamp in seconds from POSIX epoch
    """
    return (dt.replace(tzinfo=datetime.timezone.utc) - dt_utc_epoch()).total_seconds()


def dt_from_ts(ts: float) -> datetime.datetime:
    """
    Returns corresponding datetime in UTC of the given timestamp in seconds

    :param ts: timestamp in seconds from POSIX epoch

    :return: the given datetime in UTC
    """
    return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)


def dt_parse(dt_str: str, fmt_str: str | list[str] | tuple[str, ...]) -> datetime.datetime | None:
    """
    Null safely parses given string value of a datetime to the datetime instance

    :param dt_str: string value of the given datetime
    :param fmt_str: format string, or a list/tuple of format string candidates

    :return: datetime instance
    """
    if dt_str is None:
        return None

    if isinstance(fmt_str, str):
        if "%z" in fmt_str or "%Z" in fmt_str:
            return datetime.datetime.strptime(dt_str, fmt_str)
        else:
            return datetime.datetime.strptime(dt_str, fmt_str).replace(tzinfo=datetime.timezone.utc)
    elif isinstance(fmt_str, (tuple, list)):
        for s in fmt_str:
            try:
                return dt_parse(dt_str, s)
            except ValueError:
                pass
        raise ValueError("time data <%s> does not match the given formats" % dt_str)
    else:
        raise ValueError("malformed format")


def dt_format(dt: datetime.datetime, fmt_str: str) -> str | None:
    """
    Null safely formats the given datetime to a string value

    :param dt: the given datetime
    :param fmt_str: format string

    :return: string value of the given datetime
    """
    if dt is None or fmt_str is None:
        return None

    if dt.year < 1000 and "%Y" in fmt_str:
        year_str = str(dt.year).zfill(4)
        fmt_str = fmt_str.replace("%Y", year_str)

    if dt.year < 10 and "%y" in fmt_str:
        year_str = str(dt.year).zfill(2)
        fmt_str = fmt_str.replace("%y", year_str)

    return dt.strftime(fmt_str)


def dt_parse_iso(dt_str: str) -> datetime.datetime | None:
    return dt_parse(dt_str, iso_formats())


def dt_format_iso(dt: datetime.datetime) -> str | None:
    return dt_format(dt, iso_format())
