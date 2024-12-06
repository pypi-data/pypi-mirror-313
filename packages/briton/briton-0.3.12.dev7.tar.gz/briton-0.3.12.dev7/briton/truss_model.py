import asyncio
import logging
from typing import Any, Dict, List, Optional, Tuple, cast

import fastapi
from transformers import PreTrainedTokenizerFast

from briton.backend.backend_types import (
    BackendConfig,
    BatchSchedulerPolicy,
    InferBackend,
    LazyLoadParams,
    LoadParams,
)
from briton.backend.default_backend import DefaultBackend
from briton.backend.legacy_backend import LegacyBackend
from briton.briton import BritonInteractor, BritonInteractorImpl
from briton.checks import trllm_config_check
from briton.constants import (
    DEFAULT_BRITON_PORT,
    DEFAULT_MAX_FSM_WORKERS,
    OPENAI_COMPATIBLE_TAG,
    TOOL_CALL_IDS,
    TOOL_CALL_TOKENS,
)
from briton.fsm_cache import FsmCache, add_schema_to_cache
from briton.request_id_generator import RequestIdGenerator
from briton.schema import validate_model_input
from briton.secrets import get_hf_token_or_none
from briton.trtllm_build_config import (
    TrussTRTLLMBatchSchedulerPolicy,
    TrussTRTLLMBuildConfiguration,
)
from briton.truss_monitor import start_monitor

logger = logging.getLogger(__name__)


class Model:
    def __init__(self, **kwargs):
        self._loaded = False
        self._data_dir = kwargs["data_dir"]
        self._secrets = kwargs["secrets"]
        self._request_id_generator = RequestIdGenerator()
        config = kwargs["config"]
        model_metadata = config.get("model_metadata", {})
        trllm_config_check(config)
        trtllm_config = config.get("trt_llm")
        trtllm_build_config = TrussTRTLLMBuildConfiguration(**trtllm_config.get("build"))
        self._backend_config = _generate_backend_config(model_metadata, trtllm_build_config)

        self._hf_token = get_hf_token_or_none(self._secrets)
        self._lazy_init_done = False
        self._lazy_init_lock = None

        # Allow passing briton_interactor for ease of testing
        self._briton_interactor: BritonInteractor = model_metadata.get(
            "briton_interactor", BritonInteractorImpl()
        )

        # Supports passing in a backend via model_metadata
        self._backends: List[InferBackend] = model_metadata.get("infer_backends", [])
        if self._backend_config.is_openai_compatible:
            self._backends.append(DefaultBackend())
        else:
            self._backends.append(LegacyBackend())

    def load(self):
        if self._loaded:
            return

        tokenizer, added_tokens = _build_tokenizer(
            tokenizer_repo=self._backend_config.tokenizer_repo,
            hf_token=self._hf_token,
            auto_tokenizer_from_pretrained=self._briton_interactor.auto_tokenizer_from_pretrained,
        )

        # We can't do this in __init__ because tokenizer is created above in
        # load function.
        _check_or_clear_backend_config_tool_call_token(self._backend_config, tokenizer)

        self._fsm_cache = FsmCache(
            self._briton_interactor.fsm_cache_dir(),
            tokenizer,
            self._backend_config.max_fsm_workers,
            self._backend_config.tool_call_token_id,
        )

        bcfg: BackendConfig = self._backend_config
        self._briton_interactor.load(
            model_name="briton",
            engine_path=self._data_dir,
            hf_tokenizer=bcfg.tokenizer_repo,
            work_dir=self._data_dir,
            fsm_cache_dir=self._fsm_cache.cache_dir,
            kv_cache_free_gpu_mem_fraction=bcfg.kv_cache_gpu_mem_fraction,
            port=DEFAULT_BRITON_PORT,
            added_tokens=added_tokens,
            max_num_tokens=bcfg.max_num_tokens,
            enable_chunked_context=bcfg.enable_chunked_context,
            hf_token=self._hf_token,
            tp_count=bcfg.tp,
            batch_scheduler_policy=bcfg.batch_scheduler_policy.value,
        )

        for backend in self._backends:
            backend.load(
                LoadParams(
                    generate_request_id=self._request_id_generator,
                    tokenizer=tokenizer,
                    config=self._backend_config,
                )
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
                stub = self._briton_interactor.create_grpc_stub(DEFAULT_BRITON_PORT)
                await start_monitor(self._briton_interactor, self.predict, logger)

                for backend in self._backends:
                    await backend.lazy_load(LazyLoadParams(briton_stub=stub))
                self._lazy_init_done = True

        validated_input = validate_model_input(
            model_input=model_input, supports_tools=self._backend_config.tool_call_token is not None
        )

        async def _add_schema_to_cache(schema: dict) -> str:
            return await add_schema_to_cache(self._fsm_cache, schema)

        # Firt backend that accepts the request gets it
        for backend in self._backends:
            req_details = await backend.accepts_request(validated_input)
            if req_details is not None:
                # todo implement total input tokens limit here using stats
                # one issue here is including current request tokens
                # todo handle asyncio.CancelledError
                return await backend.infer(
                    model_input=validated_input,
                    is_cancelled=is_cancelled_fn,
                    add_schema_to_cache=_add_schema_to_cache,
                    request_details=req_details,
                )


def _convert_batch_scheduler_policy(
    policy: TrussTRTLLMBatchSchedulerPolicy,
) -> BatchSchedulerPolicy:
    if policy == TrussTRTLLMBatchSchedulerPolicy.MAX_UTILIZATION:
        return BatchSchedulerPolicy.MAX_UTILIZATION

    if policy == TrussTRTLLMBatchSchedulerPolicy.GUARANTEED_NO_EVICT:
        return BatchSchedulerPolicy.GUARANTEED_NO_EVICT

    logger.warning(f"Unknown batch scheduler policy: {policy}. Using GUARANTEED_NO_EVICT.")
    return BatchSchedulerPolicy.GUARANTEED_NO_EVICT


def _supports_tool_calls(tool_call_token: str, tokenizer: PreTrainedTokenizerFast) -> bool:
    if not tool_call_token:
        return False

    tool_call_token_id = tokenizer.convert_tokens_to_ids(tool_call_token)
    return tool_call_token_id != tokenizer.unk_token_id


def _check_or_clear_backend_config_tool_call_token(
    backend_config: BackendConfig, tokenizer: PreTrainedTokenizerFast
):
    if not _supports_tool_calls(backend_config.tool_call_token, tokenizer):
        backend_config.tool_call_token = None
        backend_config.tool_call_token_id = None


def _generate_backend_config(
    model_metadata: dict,
    tllm_config: TrussTRTLLMBuildConfiguration,
):
    tags = model_metadata.get("tags", [])
    enable_kv_cache_reuse = tllm_config.plugin_configuration.use_paged_context_fmha
    enable_chunked_context = tllm_config.enable_chunked_context
    batch_scheduler_policy = _convert_batch_scheduler_policy(tllm_config.batch_scheduler_policy)

    base_model = tllm_config.base_model
    tool_call_token = TOOL_CALL_TOKENS.get(base_model)
    tool_call_token_id = TOOL_CALL_IDS.get(base_model)
    is_openai_compat = OPENAI_COMPATIBLE_TAG in tags

    return BackendConfig(
        model_metadata=model_metadata,
        is_openai_compatible=is_openai_compat,
        base_model=base_model,
        tp=tllm_config.tensor_parallel_count,
        tokenizer_repo=tllm_config.checkpoint_repository.repo,
        kv_cache_gpu_mem_fraction=tllm_config.kv_cache_free_gpu_mem_fraction,
        enable_kv_cache_reuse=enable_kv_cache_reuse,
        enable_chunked_context=enable_chunked_context,
        max_num_tokens=tllm_config.max_num_tokens,
        max_seq_len=tllm_config.max_seq_len,
        batch_scheduler_policy=batch_scheduler_policy,
        default_max_tokens=tllm_config.default_max_tokens,
        max_fsm_workers=DEFAULT_MAX_FSM_WORKERS,
        tool_call_token=tool_call_token,
        tool_call_token_id=tool_call_token_id,
    )


def _build_tokenizer(
    tokenizer_repo: str,
    auto_tokenizer_from_pretrained: callable,
    hf_token: Optional[str] = None,
) -> Tuple[PreTrainedTokenizerFast, List[str]]:
    # TODO(pankaj) Support loading bundled tokenizer rather than from HF
    raw_tokenizer = auto_tokenizer_from_pretrained(tokenizer_repo, hf_token=hf_token)
    tokenizer = cast(PreTrainedTokenizerFast, raw_tokenizer)
    # We only support Llama and mistral with Briton, for which this should
    # apply.
    assert isinstance(tokenizer, PreTrainedTokenizerFast)

    # These are tokens outside of tokenizer.json. We need to pass these to
    # Briton, to pass to rust tokenizer.
    added_token_decoders = tokenizer.added_tokens_decoder
    added_tokens = list(added_token_decoders.values())

    return tokenizer, added_tokens
