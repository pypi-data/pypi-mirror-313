import math
import unittest
from decimal import Decimal

import ddt
import numpy as np

from iker.common.utils.numutils import is_nan, is_normal_real, is_real
from iker.common.utils.numutils import real_abs
from iker.common.utils.numutils import real_greater, real_nan_greater
from iker.common.utils.numutils import real_max, real_nan_max
from iker.common.utils.numutils import real_mean, real_nan_mean
from iker.common.utils.numutils import real_min, real_nan_min
from iker.common.utils.numutils import real_nan_smaller, real_smaller
from iker.common.utils.numutils import real_nan_std, real_std
from iker.common.utils.numutils import to_decimal


@ddt.ddt
class NumUtilsTest(unittest.TestCase):

    @ddt.data(
        (None, None),
        (math.nan, Decimal("nan")),
        (math.inf, Decimal("inf")),
        (-math.inf, Decimal("-inf")),
        (np.nan, Decimal("nan")),
        (np.inf, Decimal("inf")),
        (-np.inf, Decimal("-inf")),
        ("nan", Decimal("nan")),
        ("inf", Decimal("inf")),
        ("-inf", Decimal("-inf")),
        (1.0, Decimal("1.0")),
        (-1.0, Decimal("-1.0")),
        (1.0e6, Decimal("1.0e6")),
        (-1.0e-6, Decimal("-1.0e-6")),
        ("1.0", Decimal("1.0")),
        ("-1.0", Decimal("-1.0")),
        ("1.0e6", Decimal("1.0e6")),
        ("-1.0e-6", Decimal("-1.0e-6")),
        ("1.0000000000000000000000001", Decimal("1.0000000000000000000000001")),
        ("1000000000000000000000000.1", Decimal("1000000000000000000000000.1")),
    )
    @ddt.unpack
    def test_float_to_decimal(self, v, expect):
        self.assertResult(expect, to_decimal(v))

    @ddt.data(
        (None, None),
        (True, False),
        (False, False),
        (1, False),
        (0, False),
        (-1, False),
        (1e6, False),
        (0e0, False),
        (-1e-6, False),
        (float("nan"), True),
        (float("inf"), False),
        (float("-inf"), False),
        (math.nan, True),
        (math.inf, False),
        (-math.inf, False),
        (np.nan, True),
        (np.inf, False),
        (-np.inf, False),
        ("", None),
        (object(), None),
        (list(), None),
        (tuple(), None),
        (dict(), None),
    )
    @ddt.unpack
    def test_is_nan(self, v, expect):
        self.assertResult(expect, is_nan(v))

    @ddt.data(
        (None, False),
        (True, True),
        (False, True),
        (1, True),
        (0, True),
        (-1, True),
        (1e6, True),
        (0e0, True),
        (-1e-6, True),
        (float("nan"), True),
        (float("inf"), True),
        (float("-inf"), True),
        (math.nan, True),
        (math.inf, True),
        (-math.inf, True),
        (np.nan, True),
        (np.inf, True),
        (-np.inf, True),
        ("", False),
        (object(), False),
        (list(), False),
        (tuple(), False),
        (dict(), False),
    )
    @ddt.unpack
    def test_is_real(self, v, expect):
        self.assertResult(expect, is_real(v))

    @ddt.data(
        (None, False),
        (True, True),
        (False, True),
        (1, True),
        (0, True),
        (-1, True),
        (1e6, True),
        (0e0, True),
        (-1e-6, True),
        (float("nan"), False),
        (float("inf"), False),
        (float("-inf"), False),
        (math.nan, False),
        (math.inf, False),
        (-math.inf, False),
        (np.nan, False),
        (np.inf, False),
        (-np.inf, False),
        ("", False),
        (object(), False),
        (list(), False),
        (tuple(), False),
        (dict(), False),
    )
    @ddt.unpack
    def test_is_normal_real(self, v, expect):
        self.assertResult(expect, is_normal_real(v))

    @ddt.data(
        (None, None),
        (True, 1),
        (False, 0),
        (1, 1),
        (0, 0),
        (-1, 1),
        (1e6, 1e6),
        (0e0, 0),
        (-1e-6, 1e-6),
        (float("nan"), math.nan),
        (float("inf"), math.inf),
        (float("-inf"), math.inf),
        (math.nan, math.nan),
        (math.inf, math.inf),
        (-math.inf, math.inf),
        (np.nan, math.nan),
        (np.inf, math.inf),
        (-np.inf, math.inf),
        ("", None),
        (object(), None),
        (list(), None),
        (tuple(), None),
        (dict(), None),
    )
    @ddt.unpack
    def test_real_abs(self, v, expect):
        self.assertResult(expect, real_abs(v))

    @ddt.data(
        (None, None, None),
        (-1.0, None, -1.0),
        (None, 1.0, 1.0),
        (-1.0, 1.0, 1.0),
        (-1, 1.0, 1.0),
        (-1.0, 1, 1.0),
        (-1, 1, 1.0),
        (math.nan, math.nan, math.nan),
        (-1.0, math.nan, math.nan),
        (math.nan, 1.0, math.nan),
        (object(), object(), None),
        (-1.0, object(), -1.0),
        (object(), 1.0, 1.0),
        (True, False, 1.0),
    )
    @ddt.unpack
    def test_real_greater(self, a, b, expect):
        self.assertResult(expect, real_greater(a, b))

    @ddt.data(
        (None, None, None),
        (-1.0, None, -1.0),
        (None, 1.0, 1.0),
        (-1.0, 1.0, 1.0),
        (-1, 1.0, 1.0),
        (-1.0, 1, 1.0),
        (-1, 1, 1.0),
        (math.nan, math.nan, math.nan),
        (-1.0, math.nan, -1.0),
        (math.nan, 1.0, 1.0),
        (object(), object(), None),
        (-1.0, object(), -1.0),
        (object(), 1.0, 1.0),
        (True, False, 1.0),
    )
    @ddt.unpack
    def test_real_nan_greater(self, a, b, expect):
        self.assertResult(expect, real_nan_greater(a, b))

    @ddt.data(
        (None, None, None),
        (-1.0, None, -1.0),
        (None, 1.0, 1.0),
        (-1.0, 1.0, -1.0),
        (-1, 1.0, -1.0),
        (-1.0, 1, -1.0),
        (-1, 1, -1.0),
        (math.nan, math.nan, math.nan),
        (-1.0, math.nan, math.nan),
        (math.nan, 1.0, math.nan),
        (object(), object(), None),
        (-1.0, object(), -1.0),
        (object(), 1.0, 1.0),
        (True, False, 0.0),
    )
    @ddt.unpack
    def test_real_smaller(self, a, b, expect):
        self.assertResult(expect, real_smaller(a, b))

    @ddt.data(
        (None, None, None),
        (-1.0, None, -1.0),
        (None, 1.0, 1.0),
        (-1.0, 1.0, -1.0),
        (-1, 1.0, -1.0),
        (-1.0, 1, -1.0),
        (-1, 1, -1.0),
        (math.nan, math.nan, math.nan),
        (-1.0, math.nan, -1.0),
        (math.nan, 1.0, 1.0),
        (object(), object(), None),
        (-1.0, object(), -1.0),
        (object(), 1.0, 1.0),
        (True, False, 0.0),
    )
    @ddt.unpack
    def test_real_nan_smaller(self, a, b, expect):
        self.assertResult(expect, real_nan_smaller(a, b))

    @ddt.data(
        ([], None),
        ([None], None),
        ([object()], None),
        ([math.nan], math.nan),
        ([None, object(), math.nan], math.nan),
        ([None, object(), math.nan, 0.0], math.nan),
        ([None, object(), -1.0, 1.0], 1.0),
        ([-1.0, 1.0], 1.0),
        ([-1, 1.0], 1.0),
        ([-1.0, 1], 1.0),
        ([-1, 1], 1.0),
        ([True, False], 1.0),
    )
    @ddt.unpack
    def test_real_max(self, xs, expect):
        self.assertResult(expect, real_max(xs))

    @ddt.data(
        ([], None),
        ([None], None),
        ([object()], None),
        ([math.nan], math.nan),
        ([None, object(), math.nan], math.nan),
        ([None, object(), math.nan, 0.0], 0.0),
        ([None, object(), -1.0, 1.0], 1.0),
        ([-1.0, 1.0], 1.0),
        ([-1, 1.0], 1.0),
        ([-1.0, 1], 1.0),
        ([-1, 1], 1.0),
        ([True, False], 1.0),
    )
    @ddt.unpack
    def test_real_nan_max(self, xs, expect):
        self.assertResult(expect, real_nan_max(xs))

    @ddt.data(
        ([], None),
        ([None], None),
        ([object()], None),
        ([math.nan], math.nan),
        ([None, object(), math.nan], math.nan),
        ([None, object(), math.nan, 0.0], math.nan),
        ([None, object(), -1.0, 1.0], -1.0),
        ([-1.0, 1.0], -1.0),
        ([-1, 1.0], -1.0),
        ([-1.0, 1], -1.0),
        ([-1, 1], -1.0),
        ([True, False], 0.0),
    )
    @ddt.unpack
    def test_real_min(self, xs, expect):
        self.assertResult(expect, real_min(xs))

    @ddt.data(
        ([], None),
        ([None], None),
        ([object()], None),
        ([math.nan], math.nan),
        ([None, object(), math.nan], math.nan),
        ([None, object(), math.nan, 0.0], 0.0),
        ([None, object(), -1.0, 1.0], -1.0),
        ([-1.0, 1.0], -1.0),
        ([-1, 1.0], -1.0),
        ([-1.0, 1], -1.0),
        ([-1, 1], -1.0),
        ([True, False], 0.0),
    )
    @ddt.unpack
    def test_real_nan_min(self, xs, expect):
        self.assertResult(expect, real_nan_min(xs))

    @ddt.data(
        ([], None),
        ([None], None),
        ([object()], None),
        ([math.nan], math.nan),
        ([None, object(), math.nan], math.nan),
        ([None, object(), math.nan, 0.0], math.nan),
        ([None, object(), -1.0, 1.0], 0.0),
        ([-1.0, 1.0], 0.0),
        ([-1, 1.0], 0.0),
        ([-1.0, 1], 0.0),
        ([-1, 1], 0.0),
        ([True, False], 0.5),
    )
    @ddt.unpack
    def test_real_mean(self, xs, expect):
        self.assertResult(expect, real_mean(xs))

    @ddt.data(
        ([], None),
        ([None], None),
        ([object()], None),
        ([math.nan], math.nan),
        ([None, object(), math.nan], math.nan),
        ([None, object(), math.nan, 0.0], 0.0),
        ([None, object(), -1.0, 1.0], 0.0),
        ([-1.0, 1.0], 0.0),
        ([-1, 1.0], 0.0),
        ([-1.0, 1], 0.0),
        ([-1, 1], 0.0),
        ([True, False], 0.5),
    )
    @ddt.unpack
    def test_real_nan_mean(self, xs, expect):
        self.assertResult(expect, real_nan_mean(xs))

    @ddt.data(
        ([], None),
        ([None], None),
        ([object()], None),
        ([math.nan], math.nan),
        ([None, object(), math.nan], math.nan),
        ([None, object(), math.nan, 0.0], math.nan),
        ([None, object(), -1.0, 1.0], 1.0),
        ([-1.0, 1.0], 1.0),
        ([-1, 1.0], 1.0),
        ([-1.0, 1], 1.0),
        ([-1, 1], 1.0),
        ([True, False], 0.5),
    )
    @ddt.unpack
    def test_real_std(self, xs, expect):
        self.assertResult(expect, real_std(xs))

    @ddt.data(
        ([], None),
        ([None], None),
        ([object()], None),
        ([math.nan], math.nan),
        ([None, object(), math.nan], math.nan),
        ([None, object(), math.nan, 0.0], 0.0),
        ([None, object(), -1.0, 1.0], 1.0),
        ([-1.0, 1.0], 1.0),
        ([-1, 1.0], 1.0),
        ([-1.0, 1], 1.0),
        ([-1, 1], 1.0),
        ([True, False], 0.5),
    )
    @ddt.unpack
    def test_real_nan_std(self, xs, expect):
        self.assertResult(expect, real_nan_std(xs))

    def assertResult(self, expect, actual):
        if expect is None:
            self.assertIsNone(actual)
        elif is_nan(expect):
            self.assertTrue(is_nan(actual))
        else:
            self.assertEqual(expect, actual)
