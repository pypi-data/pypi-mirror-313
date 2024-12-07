import datetime
import math
import unittest
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import SupportsFloat, SupportsInt

import ddt
import pytest

from iker.common.utils.jsonutils import json_compare, json_reformat, json_sanitize


@dataclass(eq=True, frozen=True)
class PrefixedStr(object):
    prefix: str
    value: str

    def __str__(self):
        return self.prefix + "::" + self.value


@dataclass(eq=True, frozen=True)
class MultipliedInt(SupportsInt):
    value: int
    multiplier: int = 1

    def __int__(self):
        return self.value * self.multiplier


@dataclass(eq=True, frozen=True)
class MultipliedFloat(SupportsFloat):
    value: float
    multiplier: float = 1

    def __float__(self):
        return self.value * self.multiplier


@dataclass(frozen=True)
class WrappedList(Sequence):
    value: list

    def __len__(self):
        return len(self.value)

    def __getitem__(self, index):
        return self.value[index]


@dataclass(frozen=True)
class WrappedDict(Mapping):
    value: dict

    def __iter__(self):
        return iter(self.value)

    def __len__(self):
        return len(self.value)

    def __getitem__(self, index):
        return self.value[index]


@ddt.ddt
class JsonUtilsTest(unittest.TestCase):

    @ddt.data(
        (None, None),
        (True, True),
        (False, False),
        (1, 1),
        (-1, -1),
        (0, 0),
        (1.0, 1.0),
        (-1.0, -1.0),
        (0.0, 0.0),
        (1.0e9, 1.0e9),
        (-1.0e-9, -1.0e-9),
        (math.nan, math.nan),
        (math.inf, math.inf),
        (-math.inf, -math.inf),
        (MultipliedInt(-1, 100), -100),
        (MultipliedInt(1, 100), 100),
        (MultipliedFloat(1.0, 100.0), 100.0),
        (MultipliedFloat(-1.0, 100.0), -100.0),
        ("", ""),
        ("dummy", "dummy"),
        (
            [None, True, False, 1, -1, 0, 1.0, -1.0, 0.0, 1.0e9, -1.0e-9, math.nan, math.inf, -math.inf, "", "dummy"],
            [None, True, False, 1, -1, 0, 1.0, -1.0, 0.0, 1.0e9, -1.0e-9, math.nan, math.inf, -math.inf, "", "dummy"],
        ),
        (
            (None, True, False, 1, -1, 0, 1.0, -1.0, 0.0, 1.0e9, -1.0e-9, math.nan, math.inf, -math.inf, "", "dummy"),
            [None, True, False, 1, -1, 0, 1.0, -1.0, 0.0, 1.0e9, -1.0e-9, math.nan, math.inf, -math.inf, "", "dummy"],
        ),
        (
            {
                "none": None,
                "bool_true": True,
                "bool_false": False,
                "int_one": 1,
                "int_minus_one": -1,
                "int_zero": 0,
                "int_wrapped": MultipliedInt(1, -1000),
                "float_one": 1.0,
                "float_minus_one": -1.0,
                "float_zero": 0.0,
                "float_one_e_nine": 1.0e9,
                "float_minus_one_e_minus_nine": -1.0e-9,
                "float_nan": math.nan,
                "float_inf": math.inf,
                "float_minus_inf": -math.inf,
                "float_wrapped": MultipliedFloat(1.0, -1000.0),
                "str_empty": "",
                "str": "dummy",
            },
            {
                "none": None,
                "bool_true": True,
                "bool_false": False,
                "int_one": 1,
                "int_minus_one": -1,
                "int_zero": 0,
                "int_wrapped": -1000,
                "float_one": 1.0,
                "float_minus_one": -1.0,
                "float_zero": 0.0,
                "float_one_e_nine": 1.0e9,
                "float_minus_one_e_minus_nine": -1.0e-9,
                "float_nan": math.nan,
                "float_inf": math.inf,
                "float_minus_inf": -math.inf,
                "float_wrapped": -1000.0,
                "str_empty": "",
                "str": "dummy",
            },
        ),
        (
            {
                "none": None,
                "bool": {
                    "bool_true": True,
                    "bool_false": False,
                },
                "int": {
                    "int_one": 1,
                    "int_minus_one": -1,
                    "int_zero": 0,
                    "int_wrapped": MultipliedInt(1, -1000),
                },
                "float": {
                    "float_one": 1.0,
                    "float_minus_one": -1.0,
                    "float_zero": 0.0,
                    "float_one_e_nine": 1.0e9,
                    "float_minus_one_e_minus_nine": -1.0e-9,
                    "float_nan": math.nan,
                    "float_inf": math.inf,
                    "float_minus_inf": -math.inf,
                    "float_wrapped": MultipliedFloat(1.0, -1000.0),
                },
                "str": {
                    "str_empty": "",
                    "str": "dummy",
                },
                "list":
                    [None, True, False, 1, -1, 0, 1., -1., 0., 1e9, -1e-9, math.nan, math.inf, -math.inf, "", "dummy"],
                "tuple":
                    (None, True, False, 1, -1, 0, 1., -1., 0., 1e9, -1e-9, math.nan, math.inf, -math.inf, "", "dummy"),
            },
            {
                "none": None,
                "bool": {
                    "bool_true": True,
                    "bool_false": False,
                },
                "int": {
                    "int_one": 1,
                    "int_minus_one": -1,
                    "int_zero": 0,
                    "int_wrapped": -1000,
                },
                "float": {
                    "float_one": 1.0,
                    "float_minus_one": -1.0,
                    "float_zero": 0.0,
                    "float_one_e_nine": 1.0e9,
                    "float_minus_one_e_minus_nine": -1.0e-9,
                    "float_nan": math.nan,
                    "float_inf": math.inf,
                    "float_minus_inf": -math.inf,
                    "float_wrapped": -1000.0,
                },
                "str": {
                    "str_empty": "",
                    "str": "dummy",
                },
                "list":
                    [None, True, False, 1, -1, 0, 1., -1., 0., 1e9, -1e-9, math.nan, math.inf, -math.inf, "", "dummy"],
                "tuple":
                    [None, True, False, 1, -1, 0, 1., -1., 0., 1e9, -1e-9, math.nan, math.inf, -math.inf, "", "dummy"],
            },
        ),
        (
            WrappedDict({
                PrefixedStr("key", "none"): None,
                PrefixedStr("key", "bool"): WrappedDict({
                    PrefixedStr("key", "bool_true"): True,
                    PrefixedStr("key", "bool_false"): False,
                }),
                PrefixedStr("key", "int"): WrappedDict({
                    PrefixedStr("key", "int_one"): 1,
                    PrefixedStr("key", "int_minus_one"): -1,
                    PrefixedStr("key", "int_zero"): 0,
                    PrefixedStr("key", "int_wrapped"): MultipliedInt(1, -1000),
                }),
                PrefixedStr("key", "float"): WrappedDict({
                    PrefixedStr("key", "float_one"): 1.0,
                    PrefixedStr("key", "float_minus_one"): -1.0,
                    PrefixedStr("key", "float_zero"): 0.0,
                    PrefixedStr("key", "float_one_e_nine"): 1.0e9,
                    PrefixedStr("key", "float_minus_one_e_minus_nine"): -1.0e-9,
                    PrefixedStr("key", "float_nan"): math.nan,
                    PrefixedStr("key", "float_inf"): math.inf,
                    PrefixedStr("key", "float_minus_inf"): -math.inf,
                    PrefixedStr("key", "float_wrapped"): MultipliedFloat(1.0, -1000.0),
                }),
                PrefixedStr("key", "str"): WrappedDict({
                    PrefixedStr("key", "str_empty"): "",
                    PrefixedStr("key", "str"): "dummy",
                }),
                PrefixedStr("key", "list"): WrappedList(
                    [None, True, False, 1, -1, 0, 1., -1., 0., 1e9, -1e-9, math.nan, math.inf, -math.inf, "", "dummy"]),
                PrefixedStr("key", "tuple"):
                    (None, True, False, 1, -1, 0, 1., -1., 0., 1e9, -1e-9, math.nan, math.inf, -math.inf, "", "dummy"),
            }),
            {
                "key::none": None,
                "key::bool": {
                    "key::bool_true": True,
                    "key::bool_false": False,
                },
                "key::int": {
                    "key::int_one": 1,
                    "key::int_minus_one": -1,
                    "key::int_zero": 0,
                    "key::int_wrapped": -1000,
                },
                "key::float": {
                    "key::float_one": 1.0,
                    "key::float_minus_one": -1.0,
                    "key::float_zero": 0.0,
                    "key::float_one_e_nine": 1.0e9,
                    "key::float_minus_one_e_minus_nine": -1.0e-9,
                    "key::float_nan": math.nan,
                    "key::float_inf": math.inf,
                    "key::float_minus_inf": -math.inf,
                    "key::float_wrapped": -1000.0,
                },
                "key::str": {
                    "key::str_empty": "",
                    "key::str": "dummy",
                },
                "key::list":
                    [None, True, False, 1, -1, 0, 1., -1., 0., 1e9, -1e-9, math.nan, math.inf, -math.inf, "", "dummy"],
                "key::tuple":
                    [None, True, False, 1, -1, 0, 1., -1., 0., 1e9, -1e-9, math.nan, math.inf, -math.inf, "", "dummy"],
            },
        ),
    )
    @ddt.unpack
    def test_json_reformat(self, data, expect):
        self.assertTrue(json_compare(json_reformat(data), expect))

    @ddt.data(
        (set(),),
        (object(),),
        ([set(), object()],),
        ({"set": set(), "object": object()},),
    )
    def test_json_reformat__unregistered_type(self, data):
        with pytest.raises(ValueError):
            json_reformat(data)

    @ddt.data(
        (None, None),
        (True, True),
        (False, False),
        (1, 1),
        (-1, -1),
        (0, 0),
        (1.0, 1.0),
        (-1.0, -1.0),
        (0.0, 0.0),
        (1.0e9, 1.0e9),
        (-1.0e-9, -1.0e-9),
        (math.nan, "nan"),
        (math.inf, "inf"),
        (-math.inf, "-inf"),
        (MultipliedInt(-1, 100), -100),
        (MultipliedInt(1, 100), 100),
        (MultipliedFloat(1.0, 100.0), 100.0),
        (MultipliedFloat(-1.0, 100.0), -100.0),
        ("", ""),
        ("dummy", "dummy"),
        (
            datetime.datetime(2000, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc),
            "2000-01-01 00:00:00+00:00",
        ),
        (
            [None, True, False, 1, -1, 0, 1.0, -1.0, 0.0, 1.0e9, -1.0e-9, math.nan, math.inf, -math.inf, "", "dummy"],
            [None, True, False, 1, -1, 0, 1.0, -1.0, 0.0, 1.0e9, -1.0e-9, "nan", "inf", "-inf", "", "dummy"],
        ),
        (
            (None, True, False, 1, -1, 0, 1.0, -1.0, 0.0, 1.0e9, -1.0e-9, math.nan, math.inf, -math.inf, "", "dummy"),
            [None, True, False, 1, -1, 0, 1.0, -1.0, 0.0, 1.0e9, -1.0e-9, "nan", "inf", "-inf", "", "dummy"],
        ),
        ({1, 2, 3, 4, 5, 6, 7}, [1, 2, 3, 4, 5, 6, 7]),
        (
            {
                "none": None,
                "bool_true": True,
                "bool_false": False,
                "int_one": 1,
                "int_minus_one": -1,
                "int_zero": 0,
                "int_wrapped": MultipliedInt(1, -1000),
                "float_one": 1.0,
                "float_minus_one": -1.0,
                "float_zero": 0.0,
                "float_one_e_nine": 1.0e9,
                "float_minus_one_e_minus_nine": -1.0e-9,
                "float_nan": math.nan,
                "float_inf": math.inf,
                "float_minus_inf": -math.inf,
                "float_wrapped": MultipliedFloat(1.0, -1000.0),
                "str_empty": "",
                "str": "dummy",
                "datetime": datetime.datetime(2000, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc),
            },
            {
                "none": None,
                "bool_true": True,
                "bool_false": False,
                "int_one": 1,
                "int_minus_one": -1,
                "int_zero": 0,
                "int_wrapped": -1000,
                "float_one": 1.0,
                "float_minus_one": -1.0,
                "float_zero": 0.0,
                "float_one_e_nine": 1.0e9,
                "float_minus_one_e_minus_nine": -1.0e-9,
                "float_nan": "nan",
                "float_inf": "inf",
                "float_minus_inf": "-inf",
                "float_wrapped": -1000.0,
                "str_empty": "",
                "str": "dummy",
                "datetime": "2000-01-01 00:00:00+00:00",
            },
        ),
        (
            {
                "none": None,
                "bool": {
                    "bool_true": True,
                    "bool_false": False,
                },
                "int": {
                    "int_one": 1,
                    "int_minus_one": -1,
                    "int_zero": 0,
                    "int_wrapped": MultipliedInt(1, -1000),
                },
                "float": {
                    "float_one": 1.0,
                    "float_minus_one": -1.0,
                    "float_zero": 0.0,
                    "float_one_e_nine": 1.0e9,
                    "float_minus_one_e_minus_nine": -1.0e-9,
                    "float_nan": math.nan,
                    "float_inf": math.inf,
                    "float_minus_inf": -math.inf,
                    "float_wrapped": MultipliedFloat(1.0, -1000.0),
                },
                "str": {
                    "str_empty": "",
                    "str": "dummy",
                },
                "datetime": datetime.datetime(2000, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc),
                "list":
                    [None, True, False, 1, -1, 0, 1., -1., 0., 1e9, -1e-9, math.nan, math.inf, -math.inf, "", "dummy"],
                "tuple":
                    (None, True, False, 1, -1, 0, 1., -1., 0., 1e9, -1e-9, math.nan, math.inf, -math.inf, "", "dummy"),
                "set": {1, 2, 3, 4, 5, 6, 7},
            },
            {
                "none": None,
                "bool": {
                    "bool_true": True,
                    "bool_false": False,
                },
                "int": {
                    "int_one": 1,
                    "int_minus_one": -1,
                    "int_zero": 0,
                    "int_wrapped": -1000,
                },
                "float": {
                    "float_one": 1.0,
                    "float_minus_one": -1.0,
                    "float_zero": 0.0,
                    "float_one_e_nine": 1.0e9,
                    "float_minus_one_e_minus_nine": -1.0e-9,
                    "float_nan": "nan",
                    "float_inf": "inf",
                    "float_minus_inf": "-inf",
                    "float_wrapped": -1000.0,
                },
                "str": {
                    "str_empty": "",
                    "str": "dummy",
                },
                "datetime": "2000-01-01 00:00:00+00:00",
                "list": [None, True, False, 1, -1, 0, 1., -1., 0., 1e9, -1e-9, "nan", "inf", "-inf", "", "dummy"],
                "tuple": [None, True, False, 1, -1, 0, 1., -1., 0., 1e9, -1e-9, "nan", "inf", "-inf", "", "dummy"],
                "set": [1, 2, 3, 4, 5, 6, 7],
            },
        ),
        (
            WrappedDict({
                PrefixedStr("key", "none"): None,
                PrefixedStr("key", "bool"): WrappedDict({
                    PrefixedStr("key", "bool_true"): True,
                    PrefixedStr("key", "bool_false"): False,
                }),
                PrefixedStr("key", "int"): WrappedDict({
                    PrefixedStr("key", "int_one"): 1,
                    PrefixedStr("key", "int_minus_one"): -1,
                    PrefixedStr("key", "int_zero"): 0,
                    PrefixedStr("key", "int_wrapped"): MultipliedInt(1, -1000),
                }),
                PrefixedStr("key", "float"): WrappedDict({
                    PrefixedStr("key", "float_one"): 1.0,
                    PrefixedStr("key", "float_minus_one"): -1.0,
                    PrefixedStr("key", "float_zero"): 0.0,
                    PrefixedStr("key", "float_one_e_nine"): 1.0e9,
                    PrefixedStr("key", "float_minus_one_e_minus_nine"): -1.0e-9,
                    PrefixedStr("key", "float_nan"): math.nan,
                    PrefixedStr("key", "float_inf"): math.inf,
                    PrefixedStr("key", "float_minus_inf"): -math.inf,
                    PrefixedStr("key", "float_wrapped"): MultipliedFloat(1.0, -1000.0),
                }),
                PrefixedStr("key", "str"): WrappedDict({
                    PrefixedStr("key", "str_empty"): "",
                    PrefixedStr("key", "str"): "dummy",
                }),
                PrefixedStr("key", "datetime"): datetime.datetime(2000, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc),
                PrefixedStr("key", "list"): WrappedList(
                    [None, True, False, 1, -1, 0, 1., -1., 0., 1e9, -1e-9, math.nan, math.inf, -math.inf, "", "dummy"]),
                PrefixedStr("key", "tuple"):
                    (None, True, False, 1, -1, 0, 1., -1., 0., 1e9, -1e-9, math.nan, math.inf, -math.inf, "", "dummy"),
                PrefixedStr("key", "set"): {1, 2, 3, 4, 5, 6, 7},
            }),
            {
                "key::none": None,
                "key::bool": {
                    "key::bool_true": True,
                    "key::bool_false": False,
                },
                "key::int": {
                    "key::int_one": 1,
                    "key::int_minus_one": -1,
                    "key::int_zero": 0,
                    "key::int_wrapped": -1000,
                },
                "key::float": {
                    "key::float_one": 1.0,
                    "key::float_minus_one": -1.0,
                    "key::float_zero": 0.0,
                    "key::float_one_e_nine": 1.0e9,
                    "key::float_minus_one_e_minus_nine": -1.0e-9,
                    "key::float_nan": "nan",
                    "key::float_inf": "inf",
                    "key::float_minus_inf": "-inf",
                    "key::float_wrapped": -1000.0,
                },
                "key::str": {
                    "key::str_empty": "",
                    "key::str": "dummy",
                },
                "key::datetime": "2000-01-01 00:00:00+00:00",
                "key::list": [None, True, False, 1, -1, 0, 1., -1., 0., 1e9, -1e-9, "nan", "inf", "-inf", "", "dummy"],
                "key::tuple": [None, True, False, 1, -1, 0, 1., -1., 0., 1e9, -1e-9, "nan", "inf", "-inf", "", "dummy"],
                "key::set": [1, 2, 3, 4, 5, 6, 7],
            },
        ),
    )
    @ddt.unpack
    def test_json_sanitize(self, data, expect):
        self.assertTrue(json_compare(json_sanitize(data), expect))
