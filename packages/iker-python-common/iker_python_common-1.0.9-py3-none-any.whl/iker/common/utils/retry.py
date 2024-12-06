import datetime
import random
import time
from abc import ABC
from abc import abstractmethod

from iker.common.utils import logger

__all__ = [
    "Attempt",
    "Retry",
    "RetryWrapper",
    "retry",
    "retry_exponent",
    "retry_random",
]


class Attempt(object):
    def __init__(
        self,
        number: int,
        prev_wait: int,
        next_wait: int,
        start_time: datetime.datetime,
        check_time: datetime.datetime,
        last_exception: Exception,
    ):
        """
        Represents an attempt in retrying

        :param number: attempt number
        :param prev_wait: previous wait time
        :param next_wait: next wait time
        :param start_time: first attempt start time
        :param check_time: this attempt check time
        :param last_exception: exception happened in the last attempt
        """
        self.number = number
        self.prev_wait = prev_wait
        self.next_wait = next_wait
        self.start_time = start_time
        self.check_time = check_time
        self.last_exception = last_exception


class Retry(ABC):
    @abstractmethod
    def on_attempt(self, attempt: Attempt):
        """
        Updates the retry state on attempt

        :param attempt: attempt
        """
        pass

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass


class RetryWrapper(object):

    def __init__(
        self,
        cls,
        wait: int = None,
        wait_exponent_init: int = None,
        wait_exponent_max: int = None,
        wait_random_min: int = None,
        wait_random_max: int = None,
        retrials: int = None,
        timeout: int = None,
    ):
        """
        Retry executor

        :param cls: target callable
        :param wait: fixed wait between retrials
        :param wait_exponent_init: initial of exponentially increasing wait
        :param wait_exponent_max: max of exponentially increasing wait
        :param wait_random_min: min of random wait
        :param wait_random_max: max of random wait
        :param retrials: max retrials
        :param timeout: timeout
        """
        self.__wrapped = cls
        self.wait = wait
        self.wait_exponent_init = wait_exponent_init
        self.wait_exponent_max = wait_exponent_max
        self.wait_random_min = wait_random_min
        self.wait_random_max = wait_random_max
        self.retrials = retrials
        self.timeout = timeout

    def __call__(self, *args, **kwargs):
        return self.__run(*args, **kwargs)

    def __next_wait(self, attempt_number: int):
        if attempt_number <= 0:
            return None
        elif self.wait is not None:
            return self.wait
        elif self.wait_exponent_init is not None and self.wait_exponent_max is not None:
            return min(self.wait_exponent_init * (2 ** (attempt_number - 1)), self.wait_exponent_max)
        elif self.wait_random_min is not None and self.wait_random_max is not None:
            return random.randint(self.wait_random_min, self.wait_random_max)
        else:
            return 0

    def __check_timeout(self, start_time: datetime.datetime):
        now = datetime.datetime.now()
        if self.timeout is None:
            return True, now
        return (now < start_time + datetime.timedelta(seconds=self.timeout)), now

    def __run(self, *args, **kwargs):
        attempt_number = 0
        start_time = datetime.datetime.now()
        last_exception = None

        while self.retrials is None or attempt_number <= self.retrials:
            attempt_number += 1

            check_result, check_time = self.__check_timeout(start_time)
            if not check_result:
                break

            attempt = Attempt(
                attempt_number,
                self.__next_wait(attempt_number - 1),
                self.__next_wait(attempt_number),
                start_time,
                check_time,
                last_exception,
            )
            try:
                if isinstance(self.__wrapped, Retry):
                    self.__wrapped.on_attempt(attempt)
                    return self.__wrapped.execute(*args, **kwargs)
                else:
                    return self.__wrapped(*args, **kwargs)
            except Exception as e:
                logger.exception("Function target <%s> failed on attempt <%d>", self.__wrapped, attempt_number)
                last_exception = e
                time.sleep(self.__next_wait(attempt_number))

        raise RuntimeError(
            "failed to execute function target <%s> after <%d> attempts" % (self.__wrapped, attempt_number))


def retry(wait: int = None, retrials: int = None, timeout: int = None):
    def wrapper(target):
        return RetryWrapper(target, wait=wait, retrials=retrials, timeout=timeout)

    return wrapper


def retry_exponent(wait_exponent_init: int, wait_exponent_max: int, retrials: int = None, timeout: int = None):
    def wrapper(target):
        return RetryWrapper(
            target,
            wait_exponent_init=wait_exponent_init,
            wait_exponent_max=wait_exponent_max,
            retrials=retrials,
            timeout=timeout,
        )

    return wrapper


def retry_random(wait_random_min: int, wait_random_max: int, retrials: int = None, timeout: int = None):
    def wrapper(target):
        return RetryWrapper(
            target,
            wait_random_min=wait_random_min,
            wait_random_max=wait_random_max,
            retrials=retrials,
            timeout=timeout,
        )

    return wrapper
