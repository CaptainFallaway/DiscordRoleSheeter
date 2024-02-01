import asyncio
from typing import Coroutine


def sync_to_async_wrapper(func: Coroutine) -> None:
    """Decorator for running async functions in a sync context"""

    def wrapper(*args, **kwargs) -> None:
        loop = asyncio.get_event_loop()
        loop.create_task(func(*args, **kwargs))

    return wrapper
