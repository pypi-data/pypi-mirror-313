import asyncio
from logging import Logger
from typing import Awaitable, Callable, Optional

import aiohttp

from briton.async_util import predicate_with_timeout, retry_predicate
from briton.briton import BritonInteractor
from briton.constants import LOCAL_PREDICT_ENDPOINT
from briton.proc_utils import kill_current_process_and_children


async def monitor(
    monitor_fn: Callable[[], Awaitable[bool]],
    on_fail: Callable[[], None],
    should_continue: Optional[Callable[[], bool]],
    period_secs: int = 60,
    max_retries: int = 3,
    timeout_secs: int = 60,
    retry_delay_secs: int = 2,
):
    """Monitor by calling a function.
    Args:
        monitor_fn: The function to call to check.
        on_fail: Function to call when the model is unresponsive.
        should_continue: Function to determine if monitoring should continue.
        period_secs: How often to check the model.
        retries: How many times to retry.
    """
    if should_continue is None:
        should_continue = lambda: True

    while should_continue():
        if not await _check_with_timeout_and_retry(
            monitor_fn,
            timeout_secs=timeout_secs,
            max_retries=max_retries,
            retry_delay_secs=retry_delay_secs,
        ):
            on_fail()
            break
        else:
            await asyncio.sleep(period_secs)


async def _check_with_timeout_and_retry(
    monitor_fn: Callable[[], Awaitable[bool]],
    timeout_secs: int = 60,
    max_retries: int = 3,
    retry_delay_secs: int = 2,
) -> Awaitable[bool]:
    with_timeout = predicate_with_timeout(monitor_fn, timeout_secs=timeout_secs)
    with_retry = retry_predicate(with_timeout, max_retries=max_retries, delay_secs=retry_delay_secs)
    return await with_retry()


async def test_predict(logger: Logger) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                LOCAL_PREDICT_ENDPOINT,
                json={"prompt": "test", "max_tokens": 1},
            ) as response:
                if response.status == 200:
                    return True
                else:
                    logger.warning(f"Prediction test failed with status: {response.status}")
                    return False
    except Exception as e:
        logger.warning(f"Error during prediction test: {e}")
        return False


async def start_monitor(briton_interactor: BritonInteractor, logger: Logger):
    monitor_settings = briton_interactor.monitor_settings()
    if not monitor_settings.start_monitor_thread:
        return

    def on_fail():
        logger.error("Truss server is stuck, exiting truss server")
        kill_current_process_and_children()

    async def monitor_fn():
        try:
            return await test_predict(logger)
        except Exception as e:
            return False

    asyncio.create_task(
        monitor(
            monitor_fn,
            on_fail,
            monitor_settings.should_continue,
            monitor_settings.period_secs,
            monitor_settings.max_retries,
            monitor_settings.timeout_secs,
            monitor_settings.retry_delay_secs,
        )
    )
