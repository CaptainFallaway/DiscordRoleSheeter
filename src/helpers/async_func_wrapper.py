import asyncio
from typing import Any, Coroutine


def async_func_wrapper(func: Coroutine) -> None:
    """Decorator for running async functions in a sync context"""

    def wrapper(instance: Any, *args, **kwargs) -> None:
        loop = asyncio.get_event_loop()
        loop.create_task(func(instance, *args, **kwargs))

    return wrapper
