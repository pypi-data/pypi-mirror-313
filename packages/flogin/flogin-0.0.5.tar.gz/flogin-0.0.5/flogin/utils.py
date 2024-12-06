import functools
import logging
import logging.handlers
from functools import _make_key as make_cached_key
from inspect import isasyncgen, iscoroutine
from inspect import signature as _signature
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncGenerator,
    AsyncIterable,
    Awaitable,
    Callable,
    Coroutine,
    TypeVar,
)

Coro = TypeVar("Coro", bound=Callable[..., Coroutine[Any, Any, Any]])
AGenT = TypeVar("AGenT", bound=Callable[..., AsyncGenerator[Any, Any]])
T = TypeVar("T")

LOG = logging.getLogger(__name__)


class _cached_property:
    def __init__(self, function) -> None:
        self.function = function
        self.__doc__ = getattr(function, "__doc__")

    def __get__(self, instance, owner):
        if instance is None:
            return self

        value = self.function(instance)
        setattr(instance, self.function.__name__, value)

        return value


if TYPE_CHECKING:
    from functools import cached_property as cached_property
else:
    cached_property = _cached_property

__all__ = (
    "setup_logging",
    "coro_or_gen",
    "MISSING",
    "cached_property",
    "cached_coro",
    "cached_gen",
)


def copy_doc(original: Callable[..., Any]) -> Callable[[T], T]:
    def decorator(overridden: T) -> T:
        overridden.__doc__ = original.__doc__
        overridden.__signature__ = _signature(original)  # type: ignore
        return overridden

    return decorator


class _MissingSentinel:
    """A type safe sentinel used in the library to represent something as missing. Used to distinguish from ``None`` values."""

    def __bool__(self) -> bool:
        return False

    def __eq__(self, other: Any) -> bool:
        return False

    def __repr__(self) -> str:
        return "..."


MISSING: Any = _MissingSentinel()


def cached_coro(coro: Coro) -> Coro:
    r"""A decorator to cache a coro's contents based on the passed arguments. This is provided to cache search results.

    .. NOTE::
        The arguments passed to the coro must be hashable.

    Example
    --------
    .. code-block:: python3

        @plugin.search()
        @utils.cached_coro
        async def handler(query):
            ...
    """

    cache = {}

    @functools.wraps(coro)
    async def inner(*args, **kwargs):
        key = make_cached_key(args, kwargs, False)
        try:
            return cache[key]
        except KeyError:
            cache[key] = await coro_or_gen(coro(*args, **kwargs))
            return cache[key]

    return inner  # type: ignore


def cached_gen(gen: AGenT) -> AGenT:
    r"""A decorator to cache an async generator's contents based on the passed arguments. This is provided to cache search results.

    .. NOTE::
        The arguments passed to the generator must be hashable.

    Example
    --------
    .. code-block:: python3

        @plugin.search()
        @utils.cached_gen
        async def handler(query):
            ...
    """

    cache = {}

    @functools.wraps(gen)
    async def inner(*args, **kwargs):
        key = make_cached_key(args, kwargs, False)
        try:
            for item in cache[key]:
                yield item
        except KeyError:
            cache[key] = await coro_or_gen(gen(*args, **kwargs))
            for item in cache[key]:
                yield item

    return inner  # type: ignore


def setup_logging(*, formatter: logging.Formatter | None = None) -> None:
    r"""Sets up flogin's default logger.

    Parameters
    ----------
    formatter: Optional[:class:`logging.Formatter`]
        The formatter to use, incase you don't want to use the default file formatter.
    """

    level = logging.DEBUG

    handler = logging.handlers.RotatingFileHandler(
        "flogin.log", maxBytes=1000000, encoding="UTF-8"
    )

    if formatter is None:
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(
            "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
        )

    logger = logging.getLogger()
    handler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(handler)


async def coro_or_gen(coro: Awaitable[T] | AsyncIterable[T]) -> list[T] | T:
    """|coro|

    Executes an AsyncIterable or a Coroutine, and returns the result

    Parameters
    -----------
    coro: :class:`typing.Awaitable` | :class:`typing.AsyncIterable`
        The coroutine or asynciterable to be ran

    Raises
    --------
    TypeError
        Neither a :class:`typing.Coroutine` or an :class:`typing.AsyncIterable` was passed

    Returns
    --------
    Any
        Whatever was given from the :class:`typing.Coroutine` or :class:`typing.AsyncIterable`.
    """

    if iscoroutine(coro):
        return await coro
    elif isasyncgen(coro):
        return [item async for item in coro]
    else:
        raise TypeError(f"Not a coro or gen: {coro!r}")
