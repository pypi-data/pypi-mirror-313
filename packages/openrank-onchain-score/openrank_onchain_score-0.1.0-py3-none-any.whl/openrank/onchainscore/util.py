from __future__ import annotations

import asyncio
from functools import wraps

from typing import MutableMapping, Any


def set_defaults(m: MutableMapping[str, Any], /, **defaults: Any):
    for name, value in defaults.items():
        m.setdefault(name, value)


def sync(f):
    """Decorate an async function to turn it into a synchronous one.

    Done by running the function in the default asyncio loop.

    Use this, e.g. to decorate an asynchronous function to use it as
    a Click/Typer command function.
    """

    @wraps(f)
    def wrapper(*poargs, **kwargs):
        return asyncio.run(f(*poargs, **kwargs))

    return wrapper
