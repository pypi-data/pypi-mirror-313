from typing import List, Optional

from briton.backend.backend_types import RequestDetails
from briton.backend.default_backend import DefaultBackend
from briton.backend.utils import collect_text
from briton.data_structures import or_true
from briton.error_handling import grpc_error_handling
from briton.openai import remove_suffix_from_text
from briton.schema import ModelInput


class LegacyBackend(DefaultBackend):
    def __init__(self):
        super().__init__()

    # Overrides parent
    async def accepts_request(self, model_input: ModelInput) -> Optional[RequestDetails]:
        if self._config is None or self._tokenizer is None:
            return None

        if self._config.is_openai_compatible:
            return None

        input_ids = model_input.input_ids(self._tokenizer)
        return RequestDetails(input_ids=input_ids)

    # Overrides parent
    async def generate_response(
        self,
        resp_iter,
        model_input: ModelInput,
        request_id: str,
        input_ids: List[int],
        eos_token: str,
        tool_call_token: str,
    ):
        streaming = or_true(model_input.stream)
        with grpc_error_handling():
            if streaming:
                # Advance the iterator to get the first chunk, to allow any
                # validation error to be thrown. Any errors will be handled
                # gy grpc_error_handling and converted to HTTPException.
                # `first_chunk` is not discarded, it is used below.
                async for first_chunk in resp_iter:
                    break

                async def generate_processed_after_first_chunk():
                    output_text = first_chunk.output_text
                    # Try to remove tool call token from first chunk only
                    if tool_call_token is not None:
                        output_text = output_text.removeprefix(tool_call_token)
                    yield remove_suffix_from_text(
                        output_text,
                        eos_token,
                        model_input.stop,
                        model_input.skip_special_tokens,
                    )

                    async for chunk in resp_iter:
                        output_text = chunk.output_text
                        yield remove_suffix_from_text(
                            output_text,
                            eos_token,
                            model_input.stop,
                            model_input.skip_special_tokens,
                        )

                return generate_processed_after_first_chunk()
            else:
                full_text, _ = await collect_text(resp_iter)
                full_text = remove_suffix_from_text(
                    full_text,
                    eos_token,
                    model_input.stop,
                    model_input.skip_special_tokens,
                )
                if tool_call_token is not None:
                    full_text = full_text.removeprefix(tool_call_token)
                return full_text
