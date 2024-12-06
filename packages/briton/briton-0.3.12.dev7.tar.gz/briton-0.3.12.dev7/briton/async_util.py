import asyncio
from typing import Awaitable, Callable


def get_all_items(queue: asyncio.Queue):
    """Get all items from the queue without waiting."""
    items = []
    try:
        while True:
            item = queue.get_nowait()
            items.append(item)
    except asyncio.QueueEmpty:
        # Once the queue is empty, get_nowait raises QueueEmpty, and we stop
        pass
    return items


def set_event_loop_if_not_exist():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # 'RuntimeError' will be raised if there is no running loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop


def retry_predicate(
    pred: Callable[[], Awaitable[bool]],
    max_retries=5,
    delay_secs=2,
) -> Callable[[], Awaitable[bool]]:
    async def wrapper():
        for attempt in range(max_retries):
            try:
                if await pred():
                    return True
            except Exception:
                pass
            if attempt < max_retries - 1:
                await asyncio.sleep(delay_secs)
        return False

    return wrapper


def predicate_with_timeout(
    pred: Callable[[], Awaitable[bool]],
    timeout_secs: int,
) -> Callable[[], Awaitable[bool]]:
    async def wrapper():
        try:
            return await asyncio.wait_for(pred(), timeout=timeout_secs)
        except Exception:
            return False

    return wrapper
