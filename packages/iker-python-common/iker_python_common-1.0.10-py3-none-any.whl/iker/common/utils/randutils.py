import datetime
import math
import random
import string
import sys

from iker.common.utils.dtutils import dt_utc_max, dt_utc_min
from iker.common.utils.funcutils import memorized, singleton

__all__ = [
    "max_int",
    "max_float",
    "Randomizer",
    "randomizer",
]


@singleton
def max_int() -> int:
    return sys.maxsize


@singleton
def max_float() -> float:
    return sys.float_info.max


class Randomizer(object):

    def __init__(self, seed: int = 0):
        self.random = random.SystemRandom(seed)

    def next_bool(self) -> bool:
        return self.random.getrandbits(1) == 1

    def next_int(self, lo: int = 0, hi: int = max_int()) -> int:
        assert lo < hi, "The lower bound must be smaller than the upper bound"
        return self.random.randrange(lo, hi)

    def next_float(self, lo: float = 0.0, hi: float = 1.0) -> float:
        assert lo <= hi, "The lower bound must be not greater than the upper bound"
        assert not math.isinf(hi - lo), "The range between the lower bound and the upper bound exceeded the float range"
        return lo + (hi - lo) * self.random.random()

    def next_fixed(self, precision: int = 7) -> float:
        assert precision >= 0, "The precision must be non-negative"
        width = 2 ** precision
        return self.next_int(0, width) / width

    def next_gaussian(self, mu: float = 0.0, sigma: float = 1.0) -> float:
        return self.random.gauss(mu, sigma)

    def random_string(self, chars: str, length: int) -> str:
        assert length >= 0, "Length of the random string must be non-negative"
        if length == 0:
            return ""
        return "".join(self.random.choices(chars, k=length))

    def random_ascii(self, length: int) -> str:
        return self.random_string(string.ascii_letters, length)

    def random_alphanumeric(self, length: int) -> str:
        return self.random_string(string.digits + string.ascii_letters, length)

    def random_hex(self, length: int) -> str:
        # Since 'string.hexdigits' contains both lower and upper case,
        # to balance the possibility we need double the digits
        return self.random_string(string.digits + string.hexdigits, length).upper()

    def random_oct(self, length: int) -> str:
        return self.random_string(string.octdigits, length).upper()

    def random_unit_vector(self, dim: int) -> list[float]:
        assert dim > 0, "Dimension of the random unit vector must be positive"
        while True:
            v = [self.next_gaussian() for _ in range(dim)]
            n = sum(x * x for x in v) ** 0.5
            if n < 1.0e-9:
                continue
            return [x / n for x in v]

    def random_datetime(
        self,
        begin: datetime.datetime = dt_utc_min(),
        end: datetime.datetime = dt_utc_max(),
    ) -> datetime.datetime:
        return begin + datetime.timedelta(seconds=self.next_float(0.0, (end - begin).total_seconds()))

    def random_date(
        self,
        begin: datetime.date = dt_utc_min().date(),
        end: datetime.date = dt_utc_max().date(),
    ) -> datetime.date:
        dt = self.random_datetime(datetime.datetime.combine(begin, dt_utc_min().timetz()),
                                  datetime.datetime.combine(end, dt_utc_min().timetz()))
        return dt.date()

    def random_time(
        self,
        begin: datetime.time = dt_utc_min().timetz(),
        end: datetime.time = dt_utc_max().timetz(),
    ) -> datetime.time:
        dt = self.random_datetime(datetime.datetime.combine(dt_utc_min().date(), begin),
                                  datetime.datetime.combine(dt_utc_min().date(), end))
        return dt.timetz()

    def random_json_object(
        self,
        max_depth: int = 1,
        max_elems: int = 5,
        key_chars: str = string.ascii_letters,
        key_length: int = 5,
        value_chars: str = string.ascii_letters,
        value_length: int = 5,
    ) -> object:
        choices = [list, dict, int, float, bool, str, None]
        root_choices = [list, dict]
        leaf_choices = [int, float, bool, str, None]

        def generate_json_object(depth: int):
            choice = self.random.choice(choices)
            if depth == 0:
                choice = self.random.choice(root_choices)
            if depth == max_depth:
                choice = self.random.choice(leaf_choices)

            if choice == list:
                return list(generate_json_object(depth + 1) for _ in range(self.next_int(0, max_elems + 1)))
            if choice == dict:
                return dict((self.random_string(key_chars, key_length), generate_json_object(depth + 1))
                            for _ in range(self.next_int(0, max_elems + 1)))
            if choice == int:
                return self.next_int()
            if choice == float:
                return self.next_float()
            if choice == bool:
                return self.next_bool()
            if choice == str:
                return self.random_string(value_chars, value_length)

            return None

        return generate_json_object(0)


@memorized
def randomizer(seed: int = 0) -> Randomizer:
    return Randomizer(seed)
