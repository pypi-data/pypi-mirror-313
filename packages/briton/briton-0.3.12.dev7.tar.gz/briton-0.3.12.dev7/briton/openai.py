import json
import logging
import random
import time
from json import JSONDecodeError
from typing import Any, AsyncGenerator, Callable, List, Literal, Optional

import openai.types.chat.chat_completion as chat_completion
import openai.types.chat.chat_completion_chunk as chat_completion_chunk
from fastapi import HTTPException
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from openai.types.chat.chat_completion_message import ChatCompletionMessage
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)
from openai.types.completion_usage import CompletionUsage

from briton.constants import ALPHANUMERIC_CHARS

logger = logging.getLogger(__name__)


def _load_content_json(content: str) -> Any:
    """Safely load the content json from the input text."""
    try:
        return json.loads(content)
    except JSONDecodeError:
        raise HTTPException(status_code=400, detail="Tool call was cut off by max_tokens.")


def _generate_tool_call_id():
    """Mistral expects a length 9 alphanumeric id"""
    return "".join(random.choices(ALPHANUMERIC_CHARS, k=9))


def _create_tool_calls(content: str) -> List[ChatCompletionMessageToolCall]:
    content_json = _load_content_json(content)
    tool_calls = []
    for briton_fn in content_json:
        fn = Function(name=briton_fn["name"], arguments=str(briton_fn["parameters"]))
        tool_call = ChatCompletionMessageToolCall(
            id=_generate_tool_call_id(), function=fn, type="function"
        )
        tool_calls.append(tool_call)
    return tool_calls


def _finish_reason_from_text(
    text: str, eos_token: Optional[str] = None, stop_words: Optional[List[str]] = None
) -> Literal["stop", "length"]:
    if eos_token and text.endswith(eos_token):
        return "stop"
    if stop_words and text.endswith(tuple(stop_words)):
        return "stop"
    return "length"


def remove_suffix_from_text(
    text: str,
    eos_token: Optional[str] = None,
    stop_words: Optional[List[str]] = None,
    skip_special_tokens: Optional[List[str]] = None,
) -> str:
    if eos_token and text.endswith(eos_token):
        return text.removesuffix(eos_token)
    if stop_words:
        for stop_word in stop_words:
            if text.endswith(stop_word):
                return text.removesuffix(stop_word)
    # HACK (bdubayah): this could end up being very expensive.
    if skip_special_tokens:
        for special_token in skip_special_tokens:
            text = text.replace(special_token, "")
    return text


def create_completion(
    req_id: str,
    model: str,
    input_text: str,
    eos_token: Optional[str] = None,
    tool_token: Optional[str] = None,
    prompt_tokens: Optional[int] = None,
    completion_tokens: Optional[int] = None,
    stop_words: Optional[List[str]] = None,
    skip_special_tokens: Optional[List[str]] = None,
) -> ChatCompletion:
    created = int(time.time())
    finish_reason = _finish_reason_from_text(input_text, eos_token, stop_words)
    content = remove_suffix_from_text(input_text, eos_token, stop_words, skip_special_tokens)
    tool_calls = None
    if tool_token is not None and content.startswith(tool_token):
        finish_reason = "tool_calls"
        content = content.removeprefix(tool_token)
        tool_calls = _create_tool_calls(content)
        content = None
    message = ChatCompletionMessage(content=content, role="assistant", tool_calls=tool_calls)
    choice = chat_completion.Choice(finish_reason=finish_reason, index=0, message=message)
    usage = None
    if prompt_tokens is not None and completion_tokens is not None:
        usage = CompletionUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )
    return ChatCompletion(
        id=req_id,
        choices=[choice],
        created=created,
        model=model,
        object="chat.completion",
        usage=usage,
    )


def _make_sse_chunk(chunk: ChatCompletionChunk) -> str:
    return f"data: {chunk.model_dump_json()}\n\n"


# It's the responsibility of the caller to pass the full content
def _create_tool_call_deltas(
    content: str,
) -> List[chat_completion_chunk.ChoiceDeltaToolCall]:
    content_json = _load_content_json(content)
    tool_call_deltas = []
    for i, briton_fn in enumerate(content_json):
        if not (isinstance(briton_fn, dict) and "name" in briton_fn and "parameters" in briton_fn):
            logger.error(f"Generated tool calls {content_json} are not valid")
            continue
        fn = chat_completion_chunk.ChoiceDeltaToolCallFunction(
            name=briton_fn["name"], arguments=str(briton_fn["parameters"])
        )
        tool_call_delta = chat_completion_chunk.ChoiceDeltaToolCall(
            index=i, id=_generate_tool_call_id(), function=fn, type="function"
        )
        tool_call_deltas.append(tool_call_delta)
    return tool_call_deltas


def _create_completion_chunk(
    id: str,
    created: int,
    model: str,
    content: Optional[str] = None,
    role: Optional[Literal["system", "user", "assistant", "tool"]] = None,
    finish_reason: Optional[
        Literal["stop", "length", "tool_calls", "content_filter", "function_call"]
    ] = None,
    tool_calls: Optional[List[chat_completion_chunk.ChoiceDeltaToolCall]] = None,
    usage: Optional[CompletionUsage] = None,
) -> ChatCompletionChunk:
    delta = chat_completion_chunk.ChoiceDelta(content=content, role=role, tool_calls=tool_calls)
    choice = chat_completion_chunk.Choice(index=0, delta=delta, finish_reason=finish_reason)
    return ChatCompletionChunk(
        id=id,
        choices=[choice],
        created=created,
        model=model,
        object="chat.completion.chunk",
        usage=usage,
    )


async def create_completion_chunks(
    req_id: str,
    model: str,
    input_text: AsyncGenerator[str, None],
    eos_token: Optional[str] = None,
    tool_token: Optional[str] = None,
    prompt_tokens: Optional[int] = None,
    completion_tokens_fn: Optional[Callable[[], int]] = None,
    stop_words: Optional[List[str]] = None,
    skip_special_tokens: Optional[List[str]] = None,
) -> AsyncGenerator[str, None]:
    created = int(time.time())
    start_chunk = _create_completion_chunk(
        id=req_id, created=created, model=model, content="", role="assistant"
    )
    is_first_iter = True
    delta = None
    async for delta in input_text:
        if is_first_iter:
            if tool_token is not None and delta.startswith(tool_token):
                break
            is_first_iter = False
            yield _make_sse_chunk(start_chunk)
        content = remove_suffix_from_text(delta, eos_token, stop_words, skip_special_tokens)
        if len(content) == 0:
            continue  # Don't send empty chunks
        chunk = _create_completion_chunk(id=req_id, created=created, model=model, content=content)
        yield _make_sse_chunk(chunk)

    # Handle function call case
    if is_first_iter and delta is not None and tool_token and delta.startswith(tool_token):
        full_text = delta.removeprefix(tool_token)
        async for delta in input_text:
            full_text += delta
        tool_calls = _create_tool_call_deltas(
            remove_suffix_from_text(full_text, eos_token, stop_words, skip_special_tokens)
        )
        chunk = _create_completion_chunk(
            id=req_id, created=created, model=model, tool_calls=tool_calls
        )
        yield _make_sse_chunk(start_chunk)
        yield _make_sse_chunk(chunk)
        finish_reason = "tool_calls"
    else:
        finish_reason = (
            _finish_reason_from_text(delta, eos_token, stop_words)
            if delta is not None
            else "length"
        )
    end_chunk = _create_completion_chunk(
        id=req_id, created=created, model=model, finish_reason=finish_reason
    )
    yield _make_sse_chunk(end_chunk)
    if prompt_tokens is not None and completion_tokens_fn is not None:
        completion_tokens = completion_tokens_fn()
        usage = CompletionUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )
        usage_chunk = _create_completion_chunk(id=req_id, created=created, model=model, usage=usage)
        yield _make_sse_chunk(usage_chunk)
    yield "data: [DONE]\n\n"
