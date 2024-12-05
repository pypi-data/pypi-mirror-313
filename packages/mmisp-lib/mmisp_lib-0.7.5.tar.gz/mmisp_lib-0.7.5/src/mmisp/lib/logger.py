import functools
import logging
from contextvars import ContextVar
from typing import Self, TypeVar

request_log: ContextVar[list] = ContextVar("request_log")
# db_log: ContextVar[list] = ContextVar("db_log")


T = TypeVar("T")


def log(func):  # noqa
    """Log decorator for synchronous functions.

    See alog for more information.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):  # noqa
        if logger.isEnabledFor(logging.DEBUG):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            logger.debug(f"function {func.__name__} called with args {signature}")

        return func(*args, **kwargs)

    return wrapper


def alog(func):  # noqa
    """Log decorator for fastapi routes and asynchronous functions.

    Since we are using return await func, this only works for async functions
    inspect.isawaitable returns False on the decorated functions, so we cannot
    make it usable for both worlds.

    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):  # noqa
        if logger.isEnabledFor(logging.DEBUG):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            logger.debug(f"function {func.__name__} called with args {signature}")

        return await func(*args, **kwargs)

    return wrapper


class InMemoryContextHandler(logging.Handler):
    def emit(self: Self, record: logging.LogRecord) -> None:
        request_log.get([]).append(self.format(record))


def print_request_log() -> None:
    print(*request_log.get([]), sep="\n")


def reset_request_log() -> None:
    request_log.set([])


# Set up the logger
logger = logging.getLogger("mmisp")
in_memory_handler = InMemoryContextHandler()
log_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
in_memory_handler.setFormatter(log_formatter)
logger.addHandler(in_memory_handler)

sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
sqlalchemy_logger.addHandler(in_memory_handler)
