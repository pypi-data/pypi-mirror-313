import asyncio
import functools
import time
from typing import Awaitable, Callable, Coroutine, List, Optional

from briton.async_util import get_all_items
from briton.rand_util import generate_next_random_seed

ProcessorFunctionType = Callable[
    [List["SpecDecRequest"]], Coroutine[None, None, List["SpecDecRequest"]]
]


class SpecDecRequest:
    id: int
    input_ids: List[int]
    draft_ids: List[int]
    model_input: dict
    produced_token_count: int
    accepted_token_count: int
    target_time_ms: int
    draft_time_ms: int
    draft_token_count: int
    start_time: float
    iterations: int
    is_cancelled_fn: Callable[[], Awaitable[bool]]
    output_schema_hash: Optional[str]
    fsm_state: Optional[int]
    force_tools: Optional[bool]
    seed: int

    prompt_tokens: int

    def __init__(
        self,
        id: int,
        input_ids: List[int],
        draft_ids: List[int],
        model_input: dict,
        is_cancelled_fn: Callable[[], Awaitable[bool]],
        output_schema_hash: Optional[str] = None,
        force_tools: Optional[bool] = None,
        seed: int = 0,
    ):
        self.id = id
        self.input_ids = input_ids
        self.draft_ids = draft_ids
        self.model_input = model_input
        self.queue = asyncio.Queue()
        self.produced_token_count = 0
        self.accepted_token_count = 0
        self.target_time_ms = 0
        self.draft_time_ms = 0
        self.draft_token_count = 0
        self.start_time = time.time()
        self.iterations = 0
        self.is_cancelled_fn = is_cancelled_fn
        self.output_schema_hash = output_schema_hash
        self.fsm_state = None
        self.force_tools = force_tools
        self.seed = seed

        # The number of tokens in the prompt; only updated at initialization.
        self.prompt_tokens = len(self.input_ids)

    def completion_tokens(self) -> int:
        return self.produced_token_count

    def next_seed(self) -> int:
        self.seed = generate_next_random_seed(self.seed)
        return self.seed


def handle_request_exception(func):
    """Informs request async queue of the exception and returns None.

    Important to return None so it doesn't terminate the worker loop.
    """

    @functools.wraps(func)
    async def wrapper(req, *args, **kwargs):
        try:
            return await func(req, *args, **kwargs)
        except Exception as e:
            print(f"Unexpected error: {e}")
            req.queue.put_nowait(e)
            return None

    return wrapper


async def worker(
    target_queue: asyncio.Queue,
    target_processor: ProcessorFunctionType,
    draft_queue: asyncio.Queue,
    draft_processor: ProcessorFunctionType,
    stop_event: asyncio.Event,
):
    """Main loop in rail design.

    We alternate between target and draft model, reading and processing items
    from the respective queues.
    """
    while not stop_event.is_set():
        # Target
        # Wait for input
        target_item_get_task = asyncio.create_task(target_queue.get())
        stop_event_wait_task = asyncio.create_task(stop_event.wait())
        done, _ = await asyncio.wait(
            [target_item_get_task, stop_event_wait_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        if stop_event.is_set():
            print("Stopping worker")
            target_item_get_task.cancel()
            break

        for task in done:
            target_item = task.result()
            remaining_target_items = get_all_items(target_queue)
            items = [target_item] + remaining_target_items

        target_cont_items = await target_processor(items)
        for item in target_cont_items:
            draft_queue.put_nowait(item)

        # Draft
        items = get_all_items(draft_queue)
        draft_cont_items = await draft_processor(items)
        for item in draft_cont_items:
            target_queue.put_nowait(item)


def pick_tokens_from_end(num_input_ids, num_draft_max_input_tokens: int) -> int:
    """
    Draft model may have a smaller window then target. In that case we clamp to
    the shorter draft window. We do this so that the start point is stable, and
    only moves back when we go over the max.

    Net effect of this should be that we pick all tokens until just before max.
    Afterwards we start skipping first `max draft tokens // 2` tokens. And later
    more and more multiples of `max draft tokens // 2` initial tokens.

    Idea is to keep the tokens passed to draft stable, to benefit from kv cache.
    We keep at least

    Returns starting point to pick input_ids from.
    """
    half_max = num_draft_max_input_tokens // 2
    half_maxes_to_skip = max(0, ((num_input_ids - 1) // half_max) - 1)
    return half_max * half_maxes_to_skip
