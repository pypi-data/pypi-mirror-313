"""
Utility functions/coroutines for the pax25 project.
"""

import asyncio
from functools import partial
from typing import Any, Callable, Coroutine, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def async_wrap(func: Callable[P, R]) -> Callable[P, Coroutine[None, None, R]]:
    """
    Wraps a function that requires syncronous operation so it can be awaited instead
    of blocking the thread.

    Shamelessly stolen and modified from:
    https://dev.to/0xbf/turn-sync-function-to-async-python-tips-58nn
    """

    async def run(*args: P.args, **kwargs: P.kwargs) -> R:
        loop = asyncio.get_event_loop()
        part = partial(func, *args, **kwargs)
        return await loop.run_in_executor(None, part)

    return run


async def print_async(*args: Any) -> None:
    """
    Print, but async.
    """
    await async_wrap(print)(*args)


class EnumReprMixin:  # pylint: disable=too-few-public-methods
    """
    Mixin for enums that allows their export to remain copy-pastable for instantiation.
    """

    def __repr__(self) -> str:
        """
        Repr for an Enum that allows for copy-pastable instantiation.
        """
        return f"{self.__class__.__name__}.{self._name_}"  # type: ignore [attr-defined]
