import asyncio
import logging
import os
import time
from itertools import count
from typing import Any, Dict, List, Optional, cast

import fastapi
from fastapi import HTTPException as FastApiHTTPException
from transformers import PreTrainedTokenizerFast

from briton.briton import (
    BritonInteractor,
    BritonInteractorImpl,
    EosRespondingBritonInteractor,
    FailingBritonInteractor,
)
from briton.constants import (
    DEFAULT_BRITON_PORT,
    DEFAULT_MAX_FSM_WORKERS,
    DEFAULT_TP_COUNT,
    TOOL_CALL_IDS,
    TOOL_CALL_TOKENS,
)
from briton.data_structures import common_prefix_length
from briton.error_handling import grpc_error_handling
from briton.flags import TRUSS_DEVELOPMENT_MODE
from briton.fsm_cache import FsmCache, add_schema_to_cache
from briton.input_utils import set_briton_request_fields_from_model_input
from briton.openai import create_completion, create_completion_chunks
from briton.proto import Batch, InferenceRequest
from briton.schema import get_prompt, update_raw_model_input, validate_model_input
from briton.secrets import get_hf_token_or_none
from briton.spec_dec import (
    SpecDecRequest,
    handle_request_exception,
    pick_tokens_from_end,
    worker,
)
from briton.truss_monitor import start_monitor

TARGET_PORT = DEFAULT_BRITON_PORT
DRAFT_PORT = TARGET_PORT + 1

# Relative to data dir
TARGET_MODEL_PATH = "target"
DRAFT_MODEL_PATH = "draft"

logger = logging.getLogger(__name__)


class Model:
    def __init__(self, **kwargs):
        self._loaded = False
        self._model = None
        self._config = kwargs["config"]
        self._data_dir = kwargs["data_dir"]
        self._secrets = kwargs["secrets"]
        self._request_id_counter = count(start=1)
        model_metadata = self._config.get("model_metadata", {})

        self._tp_count = model_metadata.get("tp_count", DEFAULT_TP_COUNT)
        self._hf_tokenizer = _get_model_metadata_or_raise(model_metadata, "hf_tokenizer")
        self._base_model = _get_model_metadata_or_raise(model_metadata, "base_model")
        self._tool_call_token = TOOL_CALL_TOKENS.get(self._base_model)
        self._tool_call_token_id = TOOL_CALL_IDS.get(self._base_model)
        if not TRUSS_DEVELOPMENT_MODE:
            self._hf_spec_dec_repo_id = _get_model_metadata_or_raise(
                model_metadata, "hf_spec_dec_repo_id"
            )

        self._target_kv_cache_free_gpu_mem_fraction = _get_model_metadata_or_raise(
            model_metadata, "target_kv_cache_free_gpu_mem_fraction"
        )
        self._draft_kv_cache_free_gpu_mem_fraction = _get_model_metadata_or_raise(
            model_metadata, "draft_kv_cache_free_gpu_mem_fraction"
        )
        self._num_draft_max_input_tokens = _get_model_metadata_or_raise(
            model_metadata, "num_draft_max_input_tokens"
        )
        self._draft_max_num_tokens = model_metadata.get("draft_max_num_tokens", None)
        self._target_max_num_tokens = model_metadata.get("target_max_num_tokens", None)
        self._enable_chunked_context = model_metadata.get("enable_chunked_context", False)
        self._total_token_limit = model_metadata.get("total_token_limit", None)
        self._num_draft_tokens = _get_model_metadata_or_raise(model_metadata, "num_draft_tokens")
        self._hf_token = get_hf_token_or_none(self._secrets)
        self._lazy_init_done = False
        self._lazy_init_lock = None
        self._draft_stub = None
        self._target_stub = None
        self._draft_queue = None
        self._target_queue = None
        self._max_fsm_workers = DEFAULT_MAX_FSM_WORKERS

        # Total tokens input tokens in flight.
        # TODO(pankaj) Take generated tokens into account as well. That has to
        # be done carefully to avoid any performance impact. Going with this
        # simple mechanism for now.
        self._total_tokens_lock = None
        self._total_tokens = 0

        # Allow passing briton_interactor for ease of testing
        self._briton_interactor: BritonInteractor = model_metadata.get(
            "briton_interactor", BritonInteractorImpl()
        )

        # Briton interactor can also be passed as a string to pick a pre-built one
        if isinstance(self._briton_interactor, str):
            if self._briton_interactor == "EosRespondingBritonInteractor":
                logger.info("Using EosRespondingBritonInteractor")
                self._briton_interactor = EosRespondingBritonInteractor()
            elif self._briton_interactor == "FailingBritonInteractor":
                logger.info("Using FaiingBritonInteractor")
                self._briton_interactor = FailingBritonInteractor()
            else:
                raise ValueError(f"Unknown briton_interactor: {self._briton_interactor}")

    def load(self):
        if self._loaded:
            return

        if not TRUSS_DEVELOPMENT_MODE:
            self._briton_interactor.hf_download(
                self._hf_spec_dec_repo_id, local_dir=self._data_dir, hf_token=self._hf_token
            )

        # TODO(pankaj) Support loading bundled tokenizer rather than from HF
        self._tokenizer = cast(
            PreTrainedTokenizerFast,
            self._briton_interactor.auto_tokenizer_from_pretrained(
                self._hf_tokenizer, self._hf_token
            ),
        )

        # We only support Llama and mistral with Briton, for which this should
        # apply.
        assert isinstance(self._tokenizer, PreTrainedTokenizerFast)

        # These are tokens outside of tokenizer.json. We need to pass these to
        # Briton, to pass to rust tokenizer.
        added_token_decoders = self._tokenizer.added_tokens_decoder
        added_tokens = [token for token in added_token_decoders.values()]

        # Initialize n processes for _max_fsm_workers
        self._fsm_cache = FsmCache(
            self._briton_interactor.fsm_cache_dir(),
            self._tokenizer,
            self._max_fsm_workers,
            self._tool_call_token_id,
        )

        load_briton = self._briton_interactor.load
        load_briton(
            model_name="target",
            engine_path=(self._data_dir / TARGET_MODEL_PATH),
            hf_tokenizer=self._hf_tokenizer,
            work_dir=(self._data_dir / "target"),
            fsm_cache_dir=self._fsm_cache.cache_dir,
            kv_cache_free_gpu_mem_fraction=self._target_kv_cache_free_gpu_mem_fraction,
            port=TARGET_PORT,
            added_tokens=added_tokens,
            max_num_tokens=self._target_max_num_tokens,
            enable_chunked_context=self._enable_chunked_context,
            hf_token=self._hf_token,
            tp_count=self._tp_count,
        )
        load_briton(
            model_name="draft",
            engine_path=(self._data_dir / DRAFT_MODEL_PATH),
            hf_tokenizer=self._hf_tokenizer,
            work_dir=(self._data_dir / "draft"),
            fsm_cache_dir=self._fsm_cache.cache_dir,
            kv_cache_free_gpu_mem_fraction=self._target_kv_cache_free_gpu_mem_fraction,
            port=DRAFT_PORT,
            added_tokens=added_tokens,
            max_num_tokens=self._draft_max_num_tokens,
            enable_chunked_context=self._enable_chunked_context,
            hf_token=self._hf_token,
            tp_count=self._tp_count,
        )
        self._loaded = True

    async def predict(self, model_input: Dict[str, Any], request: fastapi.Request):
        """
        Run inference

        Note that the async nature of this function is a little tricky. Care is
        needed to make sure this function is a regular async function and not an
        async generator, i.e. there shouldn't be any direct yields in this
        function. This is because we need to support both streaming and
        non-streaming cases in this function. We do this by either returning an
        async-generator for the streaming case, or directly the full text for
        the other case. Returning an async generator for non-streaming case
        interferes with the open ai client proxy.
        """

        async def is_cancelled_fn():
            disconnected = await request.is_disconnected()
            if disconnected:
                logger.info("Request disconnected, cancelling.")
            return disconnected

        if not self._lazy_init_done:
            # While this isn't completely safe, the async lock needs to be
            # created within the same async loop where it will be used. Ideally,
            # the proper solution would involve supporting asynchronous load
            # function, but that is not currently supported in Truss. The risk is
            # that multiple initial requests could end up with different lock
            # instances, making the lock ineffective. In practice, this is
            # highly unlikely. This issue could occur if one request executes
            # the line below and then gets preempted, allowing another request
            # to execute the same line. However, since there is no async
            # operation in the following line, it is very unlikely for the
            # request to be preempted at that point.
            if self._lazy_init_lock is None:
                self._lazy_init_lock = asyncio.Lock()

            async with self._lazy_init_lock:
                self._total_tokens_lock = asyncio.Lock()
                self._target_stub = self._briton_interactor.create_grpc_stub(TARGET_PORT)
                self._draft_stub = self._briton_interactor.create_grpc_stub(DRAFT_PORT)
                self._target_queue = asyncio.Queue()
                self._draft_queue = asyncio.Queue()
                asyncio.create_task(
                    worker(
                        self._target_queue,
                        self._target_consumer,
                        self._draft_queue,
                        self._draft_consumer,
                        asyncio.Event(),
                    )
                )
                await start_monitor(self._briton_interactor, self.predict, logger)
                self._lazy_init_done = True

        validated_input = validate_model_input(model_input)
        prompt = get_prompt(validated_input, self._tokenizer)
        model_input.pop("messages", None)
        input_ids = self._tokenizer(prompt).input_ids
        logger.info(f"Total input tokens: {len(input_ids)}")

        request_id = self._calc_request_id()
        spec_dec_request = SpecDecRequest(
            id=request_id,
            input_ids=input_ids,
            draft_ids=[],
            model_input=model_input,
            is_cancelled_fn=is_cancelled_fn,
            seed=validated_input.seed,
        )

        schema = validated_input.output_json_schema
        if schema is not None:
            spec_dec_request.output_schema_hash = await add_schema_to_cache(self._fsm_cache, schema)
            force_tools = validated_input.force_tools
            if force_tools is not None:
                spec_dec_request.force_tools = force_tools

        update_raw_model_input(model_input, validated_input)

        # Wait for space in the total token limit.
        while self._total_tokens + len(input_ids) > self._total_token_limit:
            if await spec_dec_request.is_cancelled_fn():
                raise RuntimeError("Request cancelled")
            await asyncio.sleep(0.01)

        # Reserver space in total tokens before queueing
        async with self._total_tokens_lock:
            self._total_tokens += len(spec_dec_request.input_ids)
        self._target_queue.put_nowait(spec_dec_request)

        async def read_req_queue():
            try:
                while True:
                    inc_text = await spec_dec_request.queue.get()
                    if inc_text is None:
                        break
                    if isinstance(inc_text, FastApiHTTPException):
                        raise inc_text
                    if isinstance(inc_text, Exception):
                        raise inc_text
                    yield inc_text
            finally:
                # When done, release space from total tokens.
                async with self._total_tokens_lock:
                    self._total_tokens -= len(spec_dec_request.input_ids)

        # Get model name for openai compatibility
        model_name = validated_input.model if validated_input.model else ""

        logger.debug(f"Input ids: {input_ids}")
        if validated_input.stream:
            return create_completion_chunks(
                req_id=str(request_id),
                model=model_name,
                input_text=read_req_queue(),
                eos_token=self._eos_token(),
                tool_token=self._tool_call_token,
                prompt_tokens=(
                    spec_dec_request.prompt_tokens if validated_input.include_stream_usage else None
                ),
                completion_tokens_fn=(
                    spec_dec_request.completion_tokens
                    if validated_input.include_stream_usage
                    else None
                ),
            )
        else:
            full_text = await _collect_text(read_req_queue())
            return create_completion(
                req_id=str(request_id),
                model=model_name,
                input_text=full_text,
                eos_token=self._eos_token(),
                tool_token=self._tool_call_token,
                prompt_tokens=spec_dec_request.prompt_tokens,
                completion_tokens=spec_dec_request.completion_tokens(),
            )

    def _calc_request_id(self) -> int:
        """Calculate unique request id.

        Not thread safe, but safe to use in single threaded async context. There
        are no async operations here, so this function is unlikely to be
        preempted in the middle. This is important otherwise we may end up with
        duplicate ids.
        """
        return int(str(os.getpid()) + str(next(self._request_id_counter)))

    async def _call_draft(
        self, request_id: int, spec_dec_request: SpecDecRequest, batch_request_ids: List[int]
    ):
        """Call draft model.

        This request is part of a batch of requests. All batch requests ids need to be
        provided in batch_request_ids.
        """
        # Draft model may only support a smaller context, so limit input tokens
        # to it.
        draft_tokens_start = pick_tokens_from_end(
            len(spec_dec_request.input_ids), self._num_draft_max_input_tokens
        )
        briton_request = InferenceRequest(
            request_id=request_id,
            input_ids=spec_dec_request.input_ids[draft_tokens_start:],
            request_output_len=self._num_draft_tokens,
            batch=Batch(request_ids=batch_request_ids),
            output_schema_hash=spec_dec_request.output_schema_hash,
            fsm_state=spec_dec_request.fsm_state,
            force_tools=spec_dec_request.force_tools,
            random_seed=spec_dec_request.next_seed(),
        )
        self._update_request_end_id_pad_id(briton_request, spec_dec_request.model_input)
        with grpc_error_handling():
            resp_iter = self._draft_stub.Infer(briton_request)
            draft_output_ids = []
            async for delta in resp_iter:
                draft_output_ids.extend(delta.output_ids)
        return draft_output_ids

    async def _call_target(
        self,
        request_id: int,
        spec_dec_request: SpecDecRequest,
        batch_request_ids: List[int],
        max_tokens: Optional[int],
    ):
        """Call target model.

        This request is part of a batch of requests. All batch requests ids need to be
        provided in batch_request_ids.
        Proposed draft ids should be provided in draft_ids.
        Target model request needs all the sampling params.

        max_tokens is the maximum number of tokens to generate. Note that target model
        can generate more than one token due to draft token acceptance. max_tokens can
        be used to cut this short to adhere to the max tokens limit at request level.
        """
        request_output_len = self._num_draft_tokens + 1
        if max_tokens is not None:
            request_output_len = min(request_output_len, max_tokens)

        briton_request = InferenceRequest(
            request_id=request_id,
            input_ids=spec_dec_request.input_ids,
            draft_input_ids=spec_dec_request.draft_ids,
            request_output_len=request_output_len,
            batch=Batch(request_ids=batch_request_ids),
            output_schema_hash=spec_dec_request.output_schema_hash,
            fsm_state=spec_dec_request.fsm_state,
            force_tools=spec_dec_request.force_tools,
            write_output_states=True,  # The target should always write its state
        )
        model_input = spec_dec_request.model_input
        self._update_request_end_id_pad_id(briton_request, model_input)

        # Important this sets random_seed as well, but we override it
        # in the following line and that's important. If same same seed
        # is used for all target requests for a request, then the model
        # starts producing garbage sometimes.
        set_briton_request_fields_from_model_input(model_input, briton_request)
        briton_request.random_seed = spec_dec_request.next_seed()

        for words in ["bad_words", "stop_words"]:
            if words in model_input:
                for word in model_input[words].split(","):
                    getattr(briton_request, words).append(word)
        with grpc_error_handling():
            resp_iter = self._target_stub.Infer(briton_request)
            target_text = ""
            target_output_ids = []
            target_output_states = []

            eos_encountered = False
            max_tokens_reached = False
            async for delta in resp_iter:
                # Include the eos token, but remove anything after it.
                if self._eos_token_id() in delta.output_ids:
                    eos_token_id_index = list(delta.output_ids).index(self._eos_token_id())
                    target_output_ids.extend(delta.output_ids[: (eos_token_id_index + 1)])
                    eos_index = delta.output_text.find(self._eos_token())
                    if eos_index != -1:
                        target_text += delta.output_text[: (eos_index + len(self._eos_token()))]
                    eos_encountered = True
                    break

                target_output_ids.extend(delta.output_ids)
                target_output_states.extend(delta.output_states)

                # Note that output_text may be empty string and that's ok.
                # Briton may be buffering for unicode characters.
                target_text += delta.output_text

                # TODO(pankaj): Cut exactly at max_tokens. We let the tokens go
                # a little bit over right now as mapping subset of tokens to
                # text is a little tricky.
                # Also ideally batch manager should honor the request_output_len above
                # but it doesn't seem to in this draft acceptance case.
                if max_tokens is not None and len(target_output_ids) >= max_tokens:
                    max_tokens_reached = True
                    break

        return (
            target_output_ids,
            target_output_states,
            target_text,
            eos_encountered,
            max_tokens_reached,
        )

    def _eos_token(self):
        return getattr(self._tokenizer, "eos_token", None)

    def _eos_token_id(self):
        return getattr(self._tokenizer, "eos_token_id", None)

    def _pad_token_id(self):
        return getattr(self._tokenizer, "pad_token_id", None)

    def _update_request_end_id_pad_id(
        self, briton_request: InferenceRequest, model_input: Dict[str, Any]
    ):
        end_id = model_input.get("end_id", None) or self._eos_token_id()
        if end_id is not None:
            briton_request.end_id = end_id
        pad_id = model_input.get("pad_id", None) or self._pad_token_id()
        if pad_id is not None:
            briton_request.pad_id = pad_id

    async def _target_consumer(self, requests: List[SpecDecRequest]) -> List[SpecDecRequest]:
        """Consumes requests from the target queue and fetches predictions from target model.

        Args:
            requests (List[Request]): Requests to process

        Returns:
            List[Request]: Requests to continue.
        """

        @handle_request_exception
        async def call_target(req, req_id, batch_request_ids):
            max_tokens = req.model_input.get("max_tokens", None)
            max_incremental_target_tokens = (
                max_tokens - req.produced_token_count if max_tokens is not None else None
            )
            st = time.time()
            (
                target_output_ids,
                target_output_states,
                target_text,
                eos_encountered,
                max_tokens_reached,
            ) = await self._call_target(
                req_id,
                req,
                batch_request_ids,
                max_incremental_target_tokens,
            )
            req.target_time_ms += (time.time() - st) * 1000
            # Streaming return target_text
            req.queue.put_nowait(target_text)
            req.produced_token_count += len(target_output_ids)
            req.iterations += 1
            accepted_count = common_prefix_length(req.draft_ids, target_output_ids)
            req.accepted_token_count += accepted_count

            def should_stop():
                if eos_encountered:
                    logger.debug("eos encountered")
                    return True

                if max_tokens_reached:
                    logger.debug("Reached max tokens, stopping")
                    return True

                if len(target_output_ids) == 0:
                    logger.debug("Target output is empty, stopping")
                    return True

                return False

            # Stopping conditions and cancellation handling.
            if should_stop() or await req.is_cancelled_fn():
                logger.info(f"Total generated token count: {req.produced_token_count}")
                logger.info(f"Total draft token count: {req.draft_token_count}")
                logger.info(f"Total draft time: {req.draft_time_ms}")
                logger.info(f"Total target time: {req.target_time_ms}")
                total_time = time.time() - req.start_time
                logger.info(f"Total time: {total_time}")
                logger.info(f"TPS: {req.produced_token_count / total_time}")
                logger.info(
                    f"Avg accepted tokens count: {req.accepted_token_count / req.iterations}"
                )
                req.queue.put_nowait(None)
                return None

            req.input_ids = req.input_ids + target_output_ids
            req.fsm_state = target_output_states[-1] if len(target_output_states) > 0 else None
            return req

        # Generate all request_ids upfront
        target_request_ids = {req.id: self._calc_request_id() for req in requests}
        batch_request_ids = target_request_ids.values()
        st = time.time()
        tasks = [
            asyncio.create_task(call_target(req, target_request_ids[req.id], batch_request_ids))
            for req in requests
        ]
        cont_reqs = await asyncio.gather(*tasks)
        cont_reqs = [req for req in cont_reqs if req is not None]
        return cont_reqs

    async def _draft_consumer(self, requests: List[SpecDecRequest]):
        """Consumes requests from the draft queue and fetches predictions from draft model.

        Args:
            requests (List[Request]): Requests to process

        Returns:
            List[Request]: Requests to continue.
        """

        @handle_request_exception
        async def call_draft(req, req_id, batch_request_ids):
            st = time.time()
            draft_ids = await self._call_draft(req_id, req, batch_request_ids)
            req.draft_time_ms += (time.time() - st) * 1000
            req.draft_ids = draft_ids
            req.draft_token_count += len(draft_ids)

        draft_request_ids = {req.id: self._calc_request_id() for req in requests}
        batch_request_ids = draft_request_ids.values()
        st = time.time()
        tasks = [
            asyncio.create_task(call_draft(req, draft_request_ids[req.id], batch_request_ids))
            for req in requests
        ]
        await asyncio.gather(*tasks)
        return requests


async def _collect_text(async_text_iter):
    full_text = ""
    async for delta in async_text_iter:
        full_text += delta
    return full_text


def _get_model_metadata_or_raise(model_metadata, key):
    if key not in model_metadata:
        raise ValueError(f"{key} is required in model_metadata")
    return model_metadata[key]
