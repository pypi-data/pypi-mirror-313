from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from decimal import Decimal
from numbers import Real
from typing import Any, TypeVar

import numpy as np

__all__ = [
    "to_decimal",
    "is_nan",
    "is_real",
    "is_normal_real",
    "real_abs",
    "real_greater",
    "real_smaller",
    "real_max",
    "real_min",
    "real_mean",
    "real_std",
    "real_nan_greater",
    "real_nan_smaller",
    "real_nan_max",
    "real_nan_min",
    "real_nan_mean",
    "real_nan_std",
]

RealT = TypeVar("RealT", bound=Real)


def to_decimal(x: float | str | None) -> Decimal | None:
    return None if x is None else Decimal(str(x))


def is_nan(v: Any) -> bool | None:
    try:
        return math.isnan(v)
    except TypeError:
        return None


def is_real(v: Any) -> bool:
    return isinstance(v, Real)


def is_normal_real(v: Any) -> bool:
    return is_real(v) and not math.isnan(v) and not math.isinf(v)


def make_real_unary(
    op: Callable[[RealT], RealT],
    fb: RealT | None = None,
) -> Callable[[RealT], RealT | None]:
    def func(x: RealT) -> RealT | None:
        if not is_real(x):
            return fb
        return op(x)

    return func


def make_real_binary(
    op: Callable[[RealT, RealT], RealT],
    fb: RealT | None = None,
) -> Callable[[RealT, RealT], RealT | None]:
    def func(a: RealT, b: RealT) -> RealT | None:
        if not is_real(a) and not is_real(b):
            return fb
        if not is_real(a):
            return b
        if not is_real(b):
            return a
        return op(a, b)

    return func


def make_real_reducer(
    op: Callable[[Sequence[RealT], ...], RealT],
    fb: RealT | None = None,
) -> Callable[[Sequence[RealT], ...], RealT | None]:
    def func(xs: Sequence[RealT], *args, **kwargs) -> RealT | None:
        xs_new = list(filter(is_real, xs))
        return op(xs_new, *args, **kwargs) if len(xs_new) > 0 else fb

    return func


real_abs = make_real_unary(np.abs)
real_greater = make_real_binary(lambda x, y: np.max((x, y)))
real_smaller = make_real_binary(lambda x, y: np.min((x, y)))
real_max = make_real_reducer(np.max)
real_min = make_real_reducer(np.min)
real_mean = make_real_reducer(np.mean)
real_std = make_real_reducer(np.std)
real_nan_greater = make_real_binary(lambda x, y: np.nanmax((x, y)))
real_nan_smaller = make_real_binary(lambda x, y: np.nanmin((x, y)))
real_nan_max = make_real_reducer(np.nanmax)
real_nan_min = make_real_reducer(np.nanmin)
real_nan_mean = make_real_reducer(np.nanmean)
real_nan_std = make_real_reducer(np.nanstd)
