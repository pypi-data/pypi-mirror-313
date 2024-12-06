from typing import Any, Awaitable, Callable, Dict, List, Optional

from briton.backend.backend_types import (
    InferBackend,
    LazyLoadParams,
    LoadParams,
    RequestDetails,
)
from briton.backend.briton_request import (
    model_input_to_briton_request,
    openai_spec_response,
)
from briton.data_structures import or_false
from briton.fsm_cache import FsmCache
from briton.schema import ModelInput


class DefaultBackend(InferBackend):
    """Regular OpenAI spec support backend."""

    def __init__(self):
        self._tokenizer = None
        self._briton_stub = None
        self._generate_request_id = None
        self._config = None

    def load(self, load_params: LoadParams) -> None:
        self._tokenizer = load_params.tokenizer
        self._generate_request_id = load_params.generate_request_id
        self._config = load_params.config

    async def lazy_load(self, lazy_load_params: LazyLoadParams) -> None:
        self._briton_stub = lazy_load_params.briton_stub

    async def accepts_request(self, model_input: ModelInput) -> Optional[RequestDetails]:
        if self._config is None or self._tokenizer is None:
            return None

        if not self._config.is_openai_compatible:
            return None

        input_ids = model_input.input_ids(self._tokenizer)
        return RequestDetails(input_ids=input_ids)

    async def infer(
        self,
        model_input: ModelInput,
        is_cancelled: Callable[[], Awaitable[bool]],
        add_schema_to_cache: Callable[[Dict[str, Any]], Awaitable[str]],
        request_details: RequestDetails,
    ) -> dict:
        # TODO(pankaj) Wire up request cancellation
        input_ids = request_details.input_ids
        request_id = self._generate_request_id()
        briton_request = await model_input_to_briton_request(
            request_id=request_id,
            model_input=model_input,
            input_ids=input_ids,
            tokenizer_eos_token_id=self._tokenizer.eos_token_id,
            tokenizer_pad_token_id=self._tokenizer.pad_token_id,
            add_schema_to_cache=add_schema_to_cache,
            default_max_tokens=self._config.default_max_tokens,
            max_seq_len=self._config.max_seq_len,
        )

        resp_iter = self._briton_stub.Infer(briton_request)

        eos_token = self._tokenizer.eos_token
        tool_call_token = self._config.tool_call_token
        return await self.generate_response(
            resp_iter=resp_iter,
            model_input=model_input,
            request_id=str(request_id),
            input_ids=input_ids,
            eos_token=eos_token,
            tool_call_token=tool_call_token,
        )

    async def generate_response(
        self,
        resp_iter,
        model_input: ModelInput,
        request_id: str,
        input_ids: List[int],
        eos_token: str,
        tool_call_token: str,
    ):
        streaming = or_false(model_input.stream)
        model_name = model_input.model if model_input.model else ""
        return await openai_spec_response(
            resp_iter=resp_iter,
            request_id=request_id,
            num_input_ids=len(input_ids),
            streaming=streaming,
            eos_token=eos_token,
            tool_call_token=tool_call_token,
            model_name=model_name,
            include_stream_usage=model_input.include_stream_usage,
            stop_words=model_input.stop,
            skip_special_tokens=model_input.skip_special_tokens,
        )
