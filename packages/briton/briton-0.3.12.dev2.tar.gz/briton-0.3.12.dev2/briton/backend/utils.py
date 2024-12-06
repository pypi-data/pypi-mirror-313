from typing import List

from transformers import PreTrainedTokenizerFast

from briton.schema import ModelInput, get_prompt


async def collect_text(async_text_iter) -> tuple[str, int]:
    full_text = ""
    completion_tokens = 0
    async for delta in async_text_iter:
        completion_tokens += len(delta.output_ids)
        full_text += delta.output_text
    return full_text, completion_tokens
