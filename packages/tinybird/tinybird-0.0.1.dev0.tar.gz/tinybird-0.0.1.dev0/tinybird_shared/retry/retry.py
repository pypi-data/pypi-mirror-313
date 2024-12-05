import asyncio
import logging
import time
from functools import wraps
from typing import Any, Awaitable, Callable, Coroutine, List, Optional, Tuple, Type, TypeVar, Union

from redis.exceptions import ConnectionError
from typing_extensions import ParamSpec

RT = TypeVar("RT")
P = ParamSpec("P")


class TooManyRedisConnections(Exception):
    pass


def retry_sync(
    exception_to_check: Union[Type[Exception], Tuple[Type[Exception], ...]],
    tries: int = 10,
    delay: float = 1,
    backoff: float = 1.5,
    ch_error_codes: Optional[List[int]] = None,
) -> Callable[[Callable[P, RT]], Callable[P, RT]]:
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param exception_to_check: the exception to check. may be a tuple of
        exceptions to check
    :type exception_to_check: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: float
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: float
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance

    To be used as a function decorator, like:

    @retry_sync(Exception, tries=4)
    def test_random(text):
        x = random.random()
        if x < 0.5:
            raise Exception("Fail")
        else:
            print "Success: ", text

    """

    def deco_retry(f: Callable[P, RT]) -> Callable[P, RT]:
        @wraps(f)
        def f_retry(*args: P.args, **kwargs: P.kwargs) -> RT:
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exception_to_check as e:
                    if ch_error_codes and hasattr(e, "code") and e.code not in ch_error_codes:
                        raise
                    # https://github.com/redis/redis-py/blob/00f5be420b397adfa1b9aa9c2761f7d8a27c0a9a/redis/connection.py#L1455
                    # https://github.com/redis/redis-py/blob/00f5be420b397adfa1b9aa9c2761f7d8a27c0a9a/redis/_parsers/base.py#L51
                    if isinstance(e, ConnectionError) and (
                        "max number of clients reached" in str(e) or "Too many connections" in str(e)
                    ):
                        logging.exception(str(e))
                        raise TooManyRedisConnections()
                    logging.warning(
                        f"{str(e)} raised in function {f.__name__}, Retrying in {round(mdelay, 3)} seconds..."
                    )
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


def retry_async(
    exception_to_check: Union[Type[Exception], Tuple[Type[Exception], ...]],
    tries: int = 10,
    delay: float = 0.1,
    backoff: float = 1.1,
) -> Callable[[Callable[P, Coroutine[Any, Any, RT]]], Callable[P, Coroutine[Any, Any, RT]]]:
    def func_wrapper(f: Callable[P, Coroutine[Any, Any, RT]]) -> Callable[P, Coroutine[Any, Any, RT]]:
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> RT:
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return await f(*args, **kwargs)
                except exception_to_check as e:
                    # https://github.com/redis/redis-py/blob/00f5be420b397adfa1b9aa9c2761f7d8a27c0a9a/redis/connection.py#L1455
                    # https://github.com/redis/redis-py/blob/00f5be420b397adfa1b9aa9c2761f7d8a27c0a9a/redis/_parsers/base.py#L51
                    if isinstance(e, ConnectionError) and (
                        "max number of clients reached" in str(e) or "Too many connections" in str(e)
                    ):
                        logging.exception(str(e))
                        raise TooManyRedisConnections()
                    logging.warning(
                        f"{str(e)} raised in function {f.__name__}, Retrying in {round(mdelay, 3)} seconds..."
                    )
                    mtries -= 1
                    mdelay *= backoff
                    await asyncio.sleep(mdelay)
            return await f(*args, **kwargs)

        return wrapper

    return func_wrapper


async def retry_ondemand_async(
    f: Callable[[Callable[[], None]], Awaitable[RT]], backoff_policy: Optional[List[int]] = None
) -> RT:
    if backoff_policy is None:
        backoff_policy = [1, 3, 9]

    # Inheriting from BaseException instead of from Exception is deliberate
    # We want to avoid generic catches of Exception to catch this
    class _RetryException(BaseException):
        pass

    def retry_me() -> None:
        raise _RetryException()

    for backoff in backoff_policy:
        try:
            return await f(retry_me)
        except _RetryException:
            await asyncio.sleep(backoff)
    return await f(lambda: None)
