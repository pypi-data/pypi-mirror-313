from typing import List, Literal, Optional, Type, Union

from dataclasses import dataclass

import json

from jsonschema.exceptions import SchemaError
from jsonschema.validators import validator_for

from pydantic import BaseModel, TypeAdapter

from openai.types import CompletionCreateParams
from openai.types.chat.completion_create_params import (
    CompletionCreateParams as ChatCompletionCreateParams,
)

from nexusflowai.types import (
    NexusflowAICompletion,
    NexusflowAIChatCompletion,
    NexusflowAIChatCompletionMessage,
)
from nexusflowai.types.chat_completion import Choice as NexusflowAIChatCompletionChoice

from nexusflowai.validators.create_with_tools.preprocess import FunctionCallTranslator
from nexusflowai.validators.create_with_tools.postprocess import (
    FunctionCallResponseTranslator,
    ResponseFormatTranslator,
)


class CompletionCreateParamsNonStreaming(BaseModel):
    prompt: str
    model: str
    frequency_penalty: Optional[Literal[None]] = None
    logprobs: Optional[Literal[None]] = None
    max_tokens: Optional[int] = None
    n: Optional[Literal[1]] = None
    presence_penalty: Optional[Literal[None]] = None
    seed: Optional[Literal[None]] = None
    stop: Optional[Union[str, List[str]]] = None
    temperature: Optional[float] = None
    top_p: Optional[Union[Literal[None], Literal[1.0]]] = None
    user: str = ""
    best_of: Optional[Literal[1]] = None
    echo: Optional[Literal[False]] = None
    logit_bias: Optional[Literal[None]] = None
    suffix: Optional[Literal[None]] = None
    stream: Optional[Union[Literal[False], Literal[None]]] = False


@dataclass
class ChatCompletionToolsFlow:
    MAX_NUM_FUNCTIONS_FOR_HINT = 15

    def _validate_to_completions(
        self, create_params: ChatCompletionCreateParams, target_cls: Type[BaseModel]
    ) -> CompletionCreateParams:
        create_params = target_cls.model_validate(create_params)
        create_params = create_params.model_dump()

        ta = TypeAdapter(CompletionCreateParams)
        create_params = ta.validate_python(create_params)

        return create_params

    def preprocess(
        self, create_params: ChatCompletionCreateParams
    ) -> CompletionCreateParams:
        tools = create_params.get("tools")
        response_format = create_params.get("response_format")
        assert (
            tools or response_format
        ), "Expected at least one of `tools` or `response_format`."

        if tools:
            for tool in tools:
                function_parameters = tool["function"]["parameters"]
                schema_validator = validator_for(function_parameters)
                try:
                    schema_validator.check_schema(function_parameters)
                except SchemaError as exception:
                    raise TypeError(exception.message) from exception

        fct = FunctionCallTranslator()
        prompt = fct.create_params_to_fc_prompt(create_params)
        create_params["prompt"] = prompt

        BOT_END = "<bot_end>"
        current_stop = create_params.get("stop")
        if isinstance(current_stop, str):
            create_params["stop"] = list(set([current_stop, BOT_END]))
        elif isinstance(current_stop, list):
            create_params["stop"] = list(set(current_stop + [BOT_END]))
        else:
            create_params["stop"] = [BOT_END]

        current_temperature = create_params.get("temperature")
        if current_temperature is None:
            create_params["temperature"] = 0.0

        return self._validate_to_completions(
            create_params, CompletionCreateParamsNonStreaming
        )

    def postprocess(
        self, create_params: ChatCompletionCreateParams, response: NexusflowAICompletion
    ) -> NexusflowAIChatCompletion:
        raw_response = response.choices[0].text

        tools = create_params.get("tools")
        response_format = create_params.get("response_format")
        tool_choice = create_params.get("tool_choice")

        hints = []
        tool_calls = None
        parsed = None
        nexusflowai_extras = None
        if response_format and "extract_item" in raw_response:
            rft = ResponseFormatTranslator()
            parsed = rft.raw_response_to_parsed(response_format, raw_response)
        elif tools:
            fcrt = FunctionCallResponseTranslator()
            tool_calls = fcrt.raw_response_to_tool_calls(
                tools, raw_response, tool_choice
            )
            tool_calls = tool_calls or None
            if tool_calls is not None:
                nexusflowai_extras = json.dumps({"original_plan": raw_response})

            if len(tools) > self.MAX_NUM_FUNCTIONS_FOR_HINT:
                num_functions_hint = f"Hint: {response.model} performance is optimal within {self.MAX_NUM_FUNCTIONS_FOR_HINT} input functions!"
                hints.append(num_functions_hint)

        hints = hints or None

        return NexusflowAIChatCompletion(
            id=response.id,
            choices=[
                NexusflowAIChatCompletionChoice(
                    finish_reason="tool_calls",
                    index=0,
                    message=NexusflowAIChatCompletionMessage(
                        content=None,
                        refusal=None,
                        role="assistant",
                        tool_calls=tool_calls,
                        parsed=parsed,
                        nexusflowai_extras=nexusflowai_extras,
                    ),
                )
            ],
            created=response.created,
            model=response.model,
            object="chat.completion",
            system_fingerprint=None,
            usage=response.usage,
            hints=hints,
        )
