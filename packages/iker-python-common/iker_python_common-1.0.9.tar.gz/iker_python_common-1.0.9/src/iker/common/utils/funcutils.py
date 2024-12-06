import functools
from collections.abc import Callable
from typing import TypeVar

__all__ = [
    "singleton",
    "memorized",
    "lazy",
    "unique_returns",
]

R = TypeVar("R")


def singleton(tar: Callable[..., R] = None):
    def decorator(target):
        if not callable(target):
            raise TypeError("expected a callable")

        instance = {}

        @functools.wraps(target)
        def wrapper(*args, **kwargs):
            if target not in instance:
                instance[target] = target(*args, **kwargs)
            return instance[target]

        return wrapper

    return decorator if tar is None else decorator(tar)


def memorized(tar: Callable[..., R] = None, *, ordered: bool = False, typed: bool = False):
    def decorator(target):
        if not callable(target):
            raise TypeError("expected a callable")

        memory = {}

        def make_key(*args, **kwargs):
            if typed:
                arg_hashes = list(hash(arg) for arg in args)
            else:
                arg_hashes = list(hash((arg, type(arg))) for arg in args)
            if ordered and typed:
                kwarg_hashes = list(hash((k, v, type(v))) for k, v in kwargs.items())
            elif ordered:
                kwarg_hashes = list(hash((k, v)) for k, v in kwargs.items())
            elif typed:
                kwarg_hashes = list(hash((k, v, type(v))) for k, v in sorted(kwargs.items()))
            else:
                kwarg_hashes = list(hash((k, v)) for k, v in sorted(kwargs.items()))
            return hash(tuple(arg_hashes + kwarg_hashes))

        @functools.wraps(target)
        def wrapper(*args, **kwargs):
            hash_key = make_key(*args, **kwargs)
            if hash_key not in memory:
                memory[hash_key] = target(*args, **kwargs)
            return memory[hash_key]

        return wrapper

    return decorator if tar is None else decorator(tar)


def lazy(tar: Callable[..., R] = None):
    def decorator(target):
        if not callable(target):
            raise TypeError("expected a callable")

        @functools.wraps(target)
        def wrapper(*args, **kwargs):
            return lambda: target(*args, **kwargs)

        return wrapper

    return decorator if tar is None else decorator(tar)


def unique_returns(tar: Callable[..., R] = None, *, max_trials: int | None = None):
    def decorator(target):
        if not callable(target):
            raise TypeError("expected a callable")

        seen = set()

        @functools.wraps(target)
        def wrapper(*args, **kwargs):
            trials = 0
            while max_trials is None or trials < max_trials:
                result = target(*args, **kwargs)
                if result not in seen:
                    seen.add(result)
                    return result
                trials += 1

            raise ValueError("no unique return value found")

        return wrapper

    return decorator if tar is None else decorator(tar)
