import datetime
from typing import Any

from iker.common.utils.dtutils import dt_parse_iso
from iker.common.utils.sequtils import head, last

__all__ = [
    "is_none",
    "is_empty",
    "is_blank",
    "trim_to_none",
    "trim_to_empty",
    "parse_bool",
    "parse_bool_or",
    "parse_int_or",
    "parse_float_or",
    "parse_str_or",
    "str_conv",
    "repr_data",
    "parse_params_string",
    "strip_margin",
]


def is_none(s: str) -> bool:
    return s is None


def is_empty(s: str) -> bool:
    return is_none(s) or len(s) == 0


def is_blank(s: str) -> bool:
    return is_empty(s) or is_empty(s.strip())


def trim_to_none(s: str, chars: str | None = None) -> str | None:
    if is_none(s):
        return None
    s = s.strip(chars)
    if is_empty(s):
        return None
    return s


def trim_to_empty(s: str, chars: str = None) -> str:
    if is_none(s):
        return ""
    return s.strip(chars)


def parse_bool(v: Any) -> bool:
    if v is None:
        return False
    elif isinstance(v, (int, float)):
        return bool(v)
    elif isinstance(v, str):
        if not v:
            return False
        if v.lower() in ["true", "yes", "on", "1", "y"]:
            return True
        if v.lower() in ["false", "no", "off", "0", "n"]:
            return False
        raise ValueError("not a valid boolean literal <%s>" % v)
    elif isinstance(v, bool):
        return v
    else:
        raise ValueError("type <%s> is not convertible to bool" % type(v))


def parse_bool_or(v: Any, default: bool | None = False) -> bool | None:
    try:
        return parse_bool(v)
    except ValueError:
        return default


def parse_int_or(v: Any, default: int | None = 0) -> int | None:
    try:
        if isinstance(v, str):
            return int(v, 0)
        return int(v)
    except (TypeError, ValueError):
        return default


def parse_float_or(v: Any, default: float | None = 0.0) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def parse_str_or(v: Any, default: str | None = "") -> str | None:
    try:
        return str(v)
    except (TypeError, ValueError):
        return default


def str_conv(s: Any) -> int | float | bool | str | datetime.datetime:
    if type(s) in (int, float, bool, datetime.datetime):
        return s
    value = parse_int_or(s, None)
    if value is not None:
        return value
    value = parse_float_or(s, None)
    if value is not None:
        return value
    value = parse_bool_or(s, None)
    if value is not None:
        return value
    try:
        value = dt_parse_iso(s)
        if value is not None:
            return value
    except Exception:
        pass
    return s


def repr_data(o) -> str:
    if isinstance(o, object):
        return "{}({})".format(o.__class__.__name__, ",".join("{}={}".format(k, v) for k, v in vars(o).items()))
    return str(o)


def parse_params_string(s: str, delimiter: str = ",", kv_delimiter: str = "=") -> dict[str, str]:
    if is_blank(s):
        return {}

    result = {}
    for param in s.split(delimiter):
        segments = param.split(kv_delimiter, 1)
        if len(segments) == 1:
            result[head(segments)] = str(True)
        elif len(segments) == 2:
            result[head(segments)] = last(segments)
        else:
            raise ValueError("malformed param <%s>" % param)
    return result


def strip_margin(text: str, margin_char: str = "|") -> str:
    stripped_text = ""
    last_stripped_line = ""
    for lineno, line in enumerate(text.splitlines()):
        stripped_line = line.lstrip()
        if stripped_line.startswith(margin_char):
            stripped_line = stripped_line[len(margin_char):]
        if len(stripped_line) == 0:
            if lineno > 0:
                stripped_text += "\n"
        elif len(last_stripped_line) > 0:
            stripped_text += " " + stripped_line
        else:
            stripped_text += stripped_line
        last_stripped_line = stripped_line
    return stripped_text
