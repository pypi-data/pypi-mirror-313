import random
from functools import wraps
from typing import Any, Dict, List, Literal, Optional, Union, cast

from fastapi import HTTPException
from jinja2.exceptions import TemplateError
from pydantic import BaseModel, Field, ValidationError, model_validator
from transformers import PreTrainedTokenizerFast

from briton.constants import UINT32_MAX


def handle_tokenizer_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TemplateError) as e:
            raise HTTPException(status_code=400, detail=str(e))

    return wrapper


class ModelInput(BaseModel):
    """This class mirrors the `CompletionCreateParamsBase` in the `openai-python` repository.

    However, that class is a TypedDict rather than a pydantic model, so we redefine it here
    to take advantage of pydantic's validation features. In addition, we define helper methods
    to get the formatted prompt, tools to use, and response format to adhere to.

    Unsupported parameters:
    - https://platform.openai.com/docs/api-reference/chat/create#chat-create-store
      - OpenAI platform specific
    - https://platform.openai.com/docs/api-reference/chat/create#chat-create-metadata
      - OpenAI platform specific
    - https://platform.openai.com/docs/api-reference/chat/create#chat-create-frequency_penalty
      - Frequency penalty is not currently passed through to briton
    - https://platform.openai.com/docs/api-reference/chat/create#chat-create-logit_bias
      - User provided logit biasing is not implemented
    - https://platform.openai.com/docs/api-reference/chat/create#chat-create-logprobs
      - Returning log probabilities is not implemented
    - https://platform.openai.com/docs/api-reference/chat/create#chat-create-top_logprobs
      - Returning log probabilities is not implemented
    - https://platform.openai.com/docs/api-reference/chat/create#chat-create-n
      - Multiple generation is not implemented
    - https://platform.openai.com/docs/api-reference/chat/create#chat-create-service_tier
      - OpenAI platform specific
    - https://platform.openai.com/docs/api-reference/chat/create#chat-create-user
      - OpenAI platform specific
    - https://platform.openai.com/docs/api-reference/chat/create#chat-create-function_call
      - Deprecated
    - https://platform.openai.com/docs/api-reference/chat/create#chat-create-functions
      - Deprecated
    """

    class Tool(BaseModel):
        """An element in the top level `tools` field."""

        class Function(BaseModel):
            name: str
            description: Optional[str] = Field(None)
            parameters: Dict[str, Any]  # `parameters` holds the json schema
            return_: Optional[Dict[str, Any]] = Field(None, alias="return")

            @model_validator(mode="after")
            def definitions_valid(cls, values):
                if "definitions" in values.parameters and "$defs" in values.parameters:
                    raise ValueError(
                        "Both pydantic v1 and v2 definitions found; please check schema."
                    )
                return values

            @property
            def parameters_without_definitions(self) -> Dict[str, Any]:
                parameters = self.parameters.copy()
                for keyword in ["definitions", "$defs"]:
                    parameters.pop(keyword, None)
                return parameters

            @property
            def definitions(self) -> Optional[tuple[Dict[str, Any], str]]:
                for keyword in ["definitions", "$defs"]:
                    if keyword in self.parameters:
                        return self.parameters[keyword], keyword
                return None

            @property
            def json_schema(self) -> Dict[str, Any]:
                return {
                    "type": "object",
                    "properties": {
                        "name": {"const": self.name},
                        "parameters": self.parameters_without_definitions,
                    },
                    "required": ["name", "parameters"],
                }

        type: Literal["function"]
        function: Function

    class ToolChoice(BaseModel):
        """The top level `tool_choice` field."""

        class FunctionChoice(BaseModel):
            name: str

        type: Literal["function"]
        function: FunctionChoice

    class SchemaResponseFormat(BaseModel):
        """The top level `response_format` field."""

        class JsonSchema(BaseModel):
            """`schema_` holds the actual json schema"""

            schema_: Dict[str, Any] = Field(..., alias="schema")

        type: Literal["json_schema"]
        json_schema: JsonSchema

    class JsonResponseFormat(BaseModel):
        type: Literal["json_object"]

    class TextResponseFormat(BaseModel):
        type: Literal["text"]

    class StreamOptions(BaseModel):
        """The top level `stream_options` field."""

        include_usage: bool

    model: Optional[str] = Field("")

    # TODO: Define `Message` objects to mirror `ChatCompletionMessageParam` for validation
    messages: Optional[List[Dict[str, Any]]] = Field(None)
    prompt_: Optional[str] = Field(None, min_length=1, alias="prompt")

    max_tokens_: Optional[int] = Field(None, alias="max_tokens")
    max_completion_tokens: Optional[int] = Field(None)

    stream: Optional[bool] = Field(None)
    stream_options: Optional[StreamOptions] = Field(None)

    seed_: Optional[int] = Field(None, alias="seed")
    random_seed: Optional[int] = Field(None)

    # TODO(bdubayah) : Wire this up to briton
    frequency_penalty: Optional[float] = Field(0)
    presence_penalty: Optional[float] = Field(0)
    length_penalty: Optional[float] = Field(None)

    # Not part of openai spec but supported by briton
    repetition_penalty: Optional[float] = Field(None)

    temperature: Optional[float] = Field(1.0)
    top_p_: Optional[float] = Field(1.0, alias="top_p")
    runtime_top_p: Optional[float] = Field(None)
    top_k_: Optional[int] = Field(50, alias="top_k")
    runtime_top_k: Optional[int] = Field(None)
    stop_: Optional[Union[str, List[str]]] = Field(None, alias="stop")
    bad_words_: Optional[Union[str, List[str]]] = Field(None, alias="bad_words")
    skip_special_tokens: Optional[List[str]] = Field(None)

    response_format: Optional[
        Union[SchemaResponseFormat, JsonResponseFormat, TextResponseFormat]
    ] = Field(None)
    tools_: Optional[List[Tool]] = Field(None, alias="tools")
    tool_choice: Optional[Union[Literal["none", "required", "auto"], ToolChoice]] = Field(None)
    parallel_tool_calls: Optional[bool] = Field(True)

    beam_width: Optional[Literal[1]] = Field(None)

    end_id: Optional[int] = Field(None)
    pad_id: Optional[int] = Field(None)

    _generated_seed: Optional[int] = None

    @model_validator(mode="after")
    def top_p_valid(cls, values):
        if values.runtime_top_p is None:
            values.runtime_top_p = values.top_p_
        if values.top_p < 0 or values.top_p > 1:
            raise ValueError("`top_p` must be between 0 and 1.")
        return values

    @model_validator(mode="after")
    def top_k_valid(cls, values):
        if values.runtime_top_k is None:
            values.runtime_top_k = values.top_k_
        if values.top_k < 0:
            raise ValueError("`top_k` must be greater than or equal to 0.")
        if values.top_k is not None and values.top_k > UINT32_MAX:
            raise ValueError(f"`top_k` must be less than or equal to {UINT32_MAX}.")
        return values

    @model_validator(mode="after")
    def messages_not_empty(cls, values):
        messages = values.messages
        if messages is not None and len(messages) == 0:
            raise ValueError("`messages` cannot be empty.")
        return values

    @model_validator(mode="after")
    def oneof_messages_and_prompt_set(cls, values):
        prompt = values.prompt_
        messages = values.messages
        if prompt is None and messages is None:
            raise ValueError("One of `prompt` or `messages` must be specified.")
        if prompt is not None and messages is not None:
            raise ValueError("Only one of `prompt` and `messages` can be specified.")
        return values

    @model_validator(mode="after")
    def max_tokens_and_max_completion_tokens_not_set(cls, values):
        max_tokens = values.max_tokens_
        max_completion_tokens = values.max_completion_tokens
        if max_tokens is not None and max_completion_tokens is not None:
            raise ValueError(
                "Only one of `max_tokens` and `max_completion_tokens` can be specified."
            )
        return values

    @model_validator(mode="after")
    def tools_valid(cls, values):
        tools = values.tools_
        tool_choice = values.tool_choice
        if tools is not None and tool_choice is None:
            values.tool_choice = "auto"
        if tools is not None and len(tools) == 0 and tool_choice != "none":
            raise ValueError("`tools` cannot be empty.")
        if isinstance(tool_choice, cls.ToolChoice) and tool_choice.function.name not in [
            tool.function.name for tool in tools
        ]:
            raise ValueError("`tool_choice` not in `tools`.")
        return values

    @model_validator(mode="after")
    def tools_not_used_with_prompt(cls, values):
        prompt = values.prompt_
        tool_choice = values.tool_choice
        if prompt is not None and tool_choice is not None and tool_choice != "none":
            raise ValueError("`tool_choice` cannot be used with `prompt`.")
        return values

    @model_validator(mode="after")
    def tools_not_used_with_response_format(cls, values):
        response_format = values.response_format
        tool_choice = values.tool_choice
        if response_format is not None and tool_choice is not None and tool_choice != "none":
            raise ValueError("`tools` cannot be used with `response_format`.")
        return values

    @model_validator(mode="after")
    def temperature_ge_0(cls, values):
        if values.temperature < 0:
            raise ValueError("`temperature` must be >= 0.")
        return values

    @model_validator(mode="after")
    def adjust_temperature_for_greedy_decoding(cls, values):
        if values.temperature == 0:
            values.temperature = 0.01
            values.top_k_ = 0
            values.runtime_top_k = 0
            values.top_p_ = 0.0
            values.runtime_top_p = 0.0
        return values

    @property
    def force_tools(self) -> Optional[bool]:
        if self.tool_choice is not None and self.tool_choice != "none":
            return self.tool_choice == "required" or isinstance(self.tool_choice, self.ToolChoice)
        return None

    @property
    def tools(self) -> Optional[List[Tool]]:
        """Returns the tools to use, dependent on tool_choice."""
        if self.tool_choice is not None and self.tool_choice != "none":
            if self.tools_ is None:
                raise ValueError("`tools` must be specified with `tool_choice`.")
            if isinstance(self.tool_choice, self.ToolChoice):
                return [
                    tool
                    for tool in self.tools_
                    if tool.function.name == self.tool_choice.function.name
                ]
            return self.tools_
        return None

    @property
    def _tool_dicts(self) -> Optional[List[Dict[str, Any]]]:
        """Convenience property to get all tools as plain dicts."""
        return (
            [tool.model_dump(by_alias=True) for tool in self.tools]
            if self.tools is not None
            else None
        )

    @staticmethod
    def _create_tools_schema(
        tools: List[Tool], parallel_tool_calls: bool
    ) -> Optional[Dict[str, Any]]:
        schema = {
            "type": "array",
            "items": {"anyOf": [tool.function.json_schema for tool in tools]},
            "minItems": 1,
        }
        if not parallel_tool_calls:
            schema["maxItems"] = 1

        # This block handles moving nested definitions to the top level of the schema.
        # Because we support parallel tool calls via `anyOf`, we need to combine all
        # definitions across all tools into a single object.
        # We also have to handle the different keywords used for definitions between
        # pydantic v1 and v2.
        combined_definitions = {}
        combined_keyword = None
        for tool in tools:
            if tool.function.definitions is not None:
                definitions, keyword = tool.function.definitions
                if combined_keyword is not None and keyword != combined_keyword:
                    raise ValueError(
                        "Both pydantic v1 and v2 definitions found; please check schema."
                    )
                combined_keyword = keyword
                for name, definition in definitions.items():
                    if name in combined_definitions and combined_definitions[name] != definition:
                        raise ValueError(f"Conflicting definitions for '{name}' found.")
                    combined_definitions[name] = definition
        if combined_keyword is not None and len(combined_definitions) > 0:
            schema[combined_keyword] = combined_definitions

        return schema

    @property
    def output_json_schema(self) -> Optional[Dict[str, Any]]:
        """Creates the output json schema based on the response format or tools."""
        if isinstance(self.response_format, self.SchemaResponseFormat):
            return self.response_format.json_schema.schema_
        if isinstance(self.response_format, self.TextResponseFormat):
            return None
        if isinstance(self.response_format, self.JsonResponseFormat):
            return {}
        if self.tools is not None:
            return self._create_tools_schema(self.tools, self.parallel_tool_calls != False)
        return None

    @property
    def max_tokens(self) -> Optional[int]:
        """`max_tokens` was deprecated in favor of `max_completion_tokens`"""
        return self.max_tokens_ if self.max_tokens_ is not None else self.max_completion_tokens

    @property
    def top_p(self) -> Optional[float]:
        """`top_p` was previously named `runtime_top_p` in briton"""
        return self.runtime_top_p if self.runtime_top_p is not None else self.top_p_

    @property
    def top_k(self) -> Optional[int]:
        """`top_k` was previously named `runtime_top_k` in briton"""
        return self.runtime_top_k if self.runtime_top_k is not None else self.top_k_

    @property
    def seed(self) -> int:
        """`seed` was previously named `random_seed` in briton"""
        if self.seed_ is not None:
            return self.seed_
        if self.random_seed is not None:
            return self.random_seed
        if self._generated_seed is None:
            self._generated_seed = random.randint(-(2**63), 2**63 - 1)
        return self._generated_seed

    @property
    def include_stream_usage(self) -> bool:
        return self.stream_options is not None and self.stream_options.include_usage

    @property
    def combined_messages(self) -> List[Dict[str, Any]]:
        """Combine consecutive user messages into a single message to avoid chat template errors."""
        if not self.messages:
            return []

        combined_messages = []
        current_user_message = None

        for message in self.messages:
            if message["role"] == "user":
                if current_user_message:
                    # OpenAI combines user messages with a space and newline
                    current_user_message["content"] += f" \n{message['content']}"
                else:
                    current_user_message = message.copy()
            else:
                if current_user_message:
                    combined_messages.append(current_user_message)
                    current_user_message = None
                combined_messages.append(message)

        if current_user_message:
            combined_messages.append(current_user_message)

        return combined_messages

    @property
    def stop(self) -> Optional[List[str]]:
        if self.stop_ is None:
            return None
        if isinstance(self.stop_, str):
            return [self.stop_]
        return self.stop_

    @property
    def bad_words(self) -> Optional[List[str]]:
        if self.bad_words_ is None:
            return None
        if isinstance(self.bad_words_, str):
            return [self.bad_words_]
        return self.bad_words_

    def prompt(self, tokenizer: PreTrainedTokenizerFast) -> str:
        """Calculate text prompt from model_input.

        Prompt may be supplied in the input as such or as messages. If messages
        are supplied, they are used to generate the prompt using chat template.
        """
        if self.prompt_ is None:
            if self.messages is None:
                raise ValueError("`messages` must be specified.")
            return cast(
                str,
                tokenizer.apply_chat_template(
                    conversation=self.combined_messages,
                    tools=self._tool_dicts,
                    tokenize=False,
                    add_generation_prompt=True,
                ),
            )
        return self.prompt_

    @handle_tokenizer_exceptions
    def input_ids(self, tokenizer: PreTrainedTokenizerFast) -> List[int]:
        """Get the input ids from the prompt."""
        return tokenizer.encode(self.prompt(tokenizer), add_special_tokens=False)


class ModelInputWithoutTools(ModelInput):
    """Input class for models that don't support function calling."""

    @model_validator(mode="after")
    def tools_not_used(cls, values):
        if values.tools is not None:
            raise ValueError("This model does not support `tools`.")
        return values


def get_prompt(model_input: ModelInput, tokenizer: PreTrainedTokenizerFast) -> str:
    try:
        return model_input.prompt(tokenizer)
    except (ValueError, TemplateError) as e:
        raise HTTPException(status_code=400, detail=str(e))


def validate_model_input(model_input: Dict[str, Any], supports_tools: bool = True) -> ModelInput:
    try:
        if supports_tools:
            return ModelInput(**model_input)
        else:
            return ModelInputWithoutTools(**model_input)
    except (ValueError, ValidationError) as e:
        raise HTTPException(status_code=400, detail=str(e))


def update_raw_model_input(model_input: Dict[str, Any], validated_input: ModelInput) -> None:
    """Updates the `model_input` dictionary with values from the `validated_input` object.

    This is need in cases where 1) the field names different between the spec and briton
    and 2) where we override values (in the case of `seed` or `temperature`).

    Parameters:
    - model_input (Dict[str, Any]): The raw model input.
    - validated_input (ModelInput): The validated model input.
    """
    if validated_input.max_tokens is not None:
        model_input["max_tokens"] = validated_input.max_tokens
    if validated_input.top_k is not None:
        model_input["runtime_top_k"] = validated_input.top_k
    if validated_input.top_p is not None:
        model_input["runtime_top_p"] = validated_input.top_p
    if validated_input.temperature is not None:
        model_input["temperature"] = validated_input.temperature
    if validated_input.stop is not None:
        model_input["stop_words"] = validated_input.stop
    if validated_input.bad_words is not None:
        model_input["bad_words"] = validated_input.bad_words
    model_input["random_seed"] = validated_input.seed
