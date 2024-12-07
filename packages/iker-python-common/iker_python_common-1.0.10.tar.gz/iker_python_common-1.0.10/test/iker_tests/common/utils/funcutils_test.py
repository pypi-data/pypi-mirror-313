import unittest
from dataclasses import dataclass

import ddt
import pytest

from iker.common.utils.funcutils import lazy, memorized, singleton, unique_returns
from iker.common.utils.randutils import randomizer


@dataclass
class Counter(object):
    value: int = 0

    def call(self):
        self.value += 1


@ddt.ddt
class FuncUtilsTest(unittest.TestCase):

    def test_singleton__class(self):
        @singleton
        class DummySingleton(object):
            counter = Counter()

            def __init__(self, value):
                self.counter = Counter()
                self.counter.value = value
                DummySingleton.counter.call()

        self.assertEqual(1, DummySingleton(1).counter.value)
        self.assertEqual(1, DummySingleton.counter.value)

        # Invoked exactly once
        self.assertEqual(1, DummySingleton(2).counter.value)
        self.assertEqual(1, DummySingleton.counter.value)
        self.assertEqual(1, DummySingleton(3).counter.value)
        self.assertEqual(1, DummySingleton.counter.value)

    def test_singleton__function(self):
        @singleton
        def func(num):
            return num

        self.assertEqual(1, func(1))

        # Invoked exactly once
        self.assertEqual(1, func(2))
        self.assertEqual(1, func(3))

    def test_singleton__class_function(self):
        class DummySingleton(object):
            counter = Counter()

            def __init__(self, counter):
                self.counter = counter

            @staticmethod
            @singleton
            def get():
                DummySingleton.counter.call()
                return DummySingleton(DummySingleton.counter)

        self.assertEqual(1, DummySingleton.get().counter.value)
        self.assertEqual(1, DummySingleton.counter.value)

        # Invoked exactly once
        self.assertEqual(1, DummySingleton.get().counter.value)
        self.assertEqual(1, DummySingleton.counter.value)
        self.assertEqual(1, DummySingleton.get().counter.value)
        self.assertEqual(1, DummySingleton.counter.value)

    def test_memorized(self):
        counter = Counter()

        @memorized
        def func(a, b):
            counter.call()
            return a + b

        # Original call
        self.assertEqual(3, func(1, 2))
        self.assertEqual(3, func(1, 2))
        self.assertEqual(3, func(1, 2))

        self.assertEqual(1, counter.value)

        # New call
        self.assertEqual(3, func(2, 1))
        self.assertEqual(3, func(2, 1))
        self.assertEqual(3, func(2, 1))

        self.assertEqual(2, counter.value)

        # Another new call
        self.assertEqual(4, func(1, 3))
        self.assertEqual(4, func(1, 3))
        self.assertEqual(4, func(1, 3))

        self.assertEqual(3, counter.value)

        # Another new call with kwarg
        self.assertEqual(3, func(a=1, b=2))
        self.assertEqual(3, func(a=1, b=2))
        self.assertEqual(3, func(a=1, b=2))

        self.assertEqual(4, counter.value)

        # Another new call with the same kwarg but different order
        self.assertEqual(3, func(b=2, a=1))
        self.assertEqual(3, func(b=2, a=1))
        self.assertEqual(3, func(b=2, a=1))

        self.assertEqual(4, counter.value)

        # Another new call with the same kwarg but different type
        self.assertEqual(3, func(a=1.0, b=2.0))
        self.assertEqual(3, func(a=1.0, b=2.0))
        self.assertEqual(3, func(a=1.0, b=2.0))

        self.assertEqual(4, counter.value)

        # Another new call with the same kwarg but different order and type
        self.assertEqual(3, func(b=2.0, a=1.0))
        self.assertEqual(3, func(b=2.0, a=1.0))
        self.assertEqual(3, func(b=2.0, a=1.0))

        self.assertEqual(4, counter.value)

    def test_memorized__ordered(self):
        counter = Counter()

        @memorized(ordered=True)
        def func(a, b):
            counter.call()
            return a + b

        # Original call
        self.assertEqual(3, func(1, 2))
        self.assertEqual(3, func(1, 2))
        self.assertEqual(3, func(1, 2))

        self.assertEqual(1, counter.value)

        # New call
        self.assertEqual(3, func(2, 1))
        self.assertEqual(3, func(2, 1))
        self.assertEqual(3, func(2, 1))

        self.assertEqual(2, counter.value)

        # Another new call
        self.assertEqual(4, func(1, 3))
        self.assertEqual(4, func(1, 3))
        self.assertEqual(4, func(1, 3))

        self.assertEqual(3, counter.value)

        # Another new call with kwarg
        self.assertEqual(3, func(a=1, b=2))
        self.assertEqual(3, func(a=1, b=2))
        self.assertEqual(3, func(a=1, b=2))

        self.assertEqual(4, counter.value)

        # Another new call with the same kwarg but different order
        self.assertEqual(3, func(b=2, a=1))
        self.assertEqual(3, func(b=2, a=1))
        self.assertEqual(3, func(b=2, a=1))

        self.assertEqual(5, counter.value)

        # Another new call with the same kwarg but different type
        self.assertEqual(3, func(a=1.0, b=2.0))
        self.assertEqual(3, func(a=1.0, b=2.0))
        self.assertEqual(3, func(a=1.0, b=2.0))

        self.assertEqual(5, counter.value)

        # Another new call with the same kwarg but different order and type
        self.assertEqual(3, func(b=2.0, a=1.0))
        self.assertEqual(3, func(b=2.0, a=1.0))
        self.assertEqual(3, func(b=2.0, a=1.0))

        self.assertEqual(5, counter.value)

    def test_memorized__typed(self):
        counter = Counter()

        @memorized(typed=True)
        def func(a, b):
            counter.call()
            return a + b

        # Original call
        self.assertEqual(3, func(1, 2))
        self.assertEqual(3, func(1, 2))
        self.assertEqual(3, func(1, 2))

        self.assertEqual(1, counter.value)

        # New call
        self.assertEqual(3, func(2, 1))
        self.assertEqual(3, func(2, 1))
        self.assertEqual(3, func(2, 1))

        self.assertEqual(2, counter.value)

        # Another new call
        self.assertEqual(4, func(1, 3))
        self.assertEqual(4, func(1, 3))
        self.assertEqual(4, func(1, 3))

        self.assertEqual(3, counter.value)

        # Another new call with kwarg
        self.assertEqual(3, func(a=1, b=2))
        self.assertEqual(3, func(a=1, b=2))
        self.assertEqual(3, func(a=1, b=2))

        self.assertEqual(4, counter.value)

        # Another new call with the same kwarg but different order
        self.assertEqual(3, func(b=2, a=1))
        self.assertEqual(3, func(b=2, a=1))
        self.assertEqual(3, func(b=2, a=1))

        self.assertEqual(4, counter.value)

        # Another new call with the same kwarg but different type
        self.assertEqual(3, func(a=1.0, b=2.0))
        self.assertEqual(3, func(a=1.0, b=2.0))
        self.assertEqual(3, func(a=1.0, b=2.0))

        self.assertEqual(5, counter.value)

        # Another new call with the same kwarg but different order and type
        self.assertEqual(3, func(b=2.0, a=1.0))
        self.assertEqual(3, func(b=2.0, a=1.0))
        self.assertEqual(3, func(b=2.0, a=1.0))

        self.assertEqual(5, counter.value)

    def test_memorized__ordered_typed(self):
        counter = Counter()

        @memorized(ordered=True, typed=True)
        def func(a, b):
            counter.call()
            return a + b

        # Original call
        self.assertEqual(3, func(1, 2))
        self.assertEqual(3, func(1, 2))
        self.assertEqual(3, func(1, 2))

        self.assertEqual(1, counter.value)

        # New call
        self.assertEqual(3, func(2, 1))
        self.assertEqual(3, func(2, 1))
        self.assertEqual(3, func(2, 1))

        self.assertEqual(2, counter.value)

        # Another new call
        self.assertEqual(4, func(1, 3))
        self.assertEqual(4, func(1, 3))
        self.assertEqual(4, func(1, 3))

        self.assertEqual(3, counter.value)

        # Another new call with kwarg
        self.assertEqual(3, func(a=1, b=2))
        self.assertEqual(3, func(a=1, b=2))
        self.assertEqual(3, func(a=1, b=2))

        self.assertEqual(4, counter.value)

        # Another new call with the same kwarg but different order
        self.assertEqual(3, func(b=2, a=1))
        self.assertEqual(3, func(b=2, a=1))
        self.assertEqual(3, func(b=2, a=1))

        self.assertEqual(5, counter.value)

        # Another new call with the same kwarg but different type
        self.assertEqual(3, func(a=1.0, b=2.0))
        self.assertEqual(3, func(a=1.0, b=2.0))
        self.assertEqual(3, func(a=1.0, b=2.0))

        self.assertEqual(6, counter.value)

        # Another new call with the same kwarg but different order and type
        self.assertEqual(3, func(b=2.0, a=1.0))
        self.assertEqual(3, func(b=2.0, a=1.0))
        self.assertEqual(3, func(b=2.0, a=1.0))

        self.assertEqual(7, counter.value)

    def test_lazy(self):
        counter = Counter()

        @lazy
        def func(a, b):
            counter.call()
            return a + b

        lazy_call = func(1, 2)

        self.assertEqual(0, counter.value)

        self.assertEqual(3, lazy_call())
        self.assertEqual(3, lazy_call())
        self.assertEqual(3, lazy_call())

        self.assertEqual(3, counter.value)

    def test_lazy__with_memorized(self):
        counter = Counter()

        @lazy
        @memorized
        def func(a, b):
            counter.call()
            return a + b

        lazy_call = func(1, 2)

        self.assertEqual(0, counter.value)

        # Original call
        self.assertEqual(3, lazy_call())
        self.assertEqual(3, lazy_call())
        self.assertEqual(3, lazy_call())

        self.assertEqual(1, counter.value)

        # A new call
        self.assertEqual(3, func(2, 1)())
        self.assertEqual(3, func(2, 1)())
        self.assertEqual(3, func(2, 1)())

        self.assertEqual(2, counter.value)

        # Another new call
        self.assertEqual(4, func(1, 3)())
        self.assertEqual(4, func(1, 3)())
        self.assertEqual(4, func(1, 3)())

        self.assertEqual(3, counter.value)

    def test_unique_returns(self):
        for _ in range(0, 100000):
            rng = randomizer()

            @unique_returns
            def func(a, b):
                return rng.next_int(a, b)

            lo = rng.next_int(0, 100)
            hi = rng.next_int(100, 200)

            result = [func(lo, hi) for _ in range(hi, lo)]
            self.assertEqual(set(result), set(range(hi, lo)))

    def test_unique_returns__mex_trial_exceeded(self):
        rng = randomizer()

        def func(a, b):
            return rng.next_int(a, b)

        decorated_func = unique_returns(func, max_trials=10)

        with pytest.raises(ValueError):
            [decorated_func(0, 10) for _ in range(11)]
