from typing import Union

from dataclasses import dataclass

import json

from openai._types import NOT_GIVEN
from openai.types.chat.completion_create_params import (
    CompletionCreateParams as ChatCompletionCreateParams,
)
from openai.types.completion_create_params import CompletionCreateParams

from nexusflowai.validators.base_input_validator import BaseInputValidator
from nexusflowai._exceptions import DeprecationError
from nexusflowai.validators.json_schema_to_dataclasses import (
    try_convert_to_dataclasses_str,
)


@dataclass
class ChatCompletionsInputValidator(BaseInputValidator):
    def validate(self) -> ChatCompletionCreateParams:
        tools = self.request_body["tools"]
        has_tools = tools is not NOT_GIVEN and bool(tools)
        has_response_format = self.request_body["response_format"] is not NOT_GIVEN

        if has_tools and has_response_format:
            raise NotImplementedError(
                "Using `tools` and `response_format` is currently not supported!"
            )

        self._validate_stream(params=self.request_body)

        self._validate_stop_token(params=self.request_body)

        self._check_for_unsupported_parameter_value(
            params=self.request_body,
            parameter_name="function_call",
            supported_value=NOT_GIVEN,
            exception_class=DeprecationError,
            exception_message="The function_call parameter is deprecated",
        )
        self._check_for_unsupported_parameter_value(
            params=self.request_body,
            parameter_name="functions",
            supported_value=NOT_GIVEN,
            exception_class=DeprecationError,
            exception_message="The functions parameter is deprecated in favor of tools",
        )

        self._check_for_unsupported_parameter_value(
            params=self.request_body,
            parameter_name="n",
            exception_class=NotImplementedError,
            supported_value=1,
            assign_supported_value=True,
        )

        self._validate_temperature(params=self.request_body)

        self._validate_response_format(params=self.request_body)

        return self.request_body

    @classmethod
    def _validate_stream(
        cls, params: Union[ChatCompletionCreateParams, CompletionCreateParams]
    ):
        if not params["stream"]:
            return

        if params.get("tools", []):
            raise AssertionError("Streaming is not supported with tools!")
        if params.get("response_format"):
            raise AssertionError("Streaming is not supported with response format!")

    @classmethod
    def _validate_response_format(cls, params: ChatCompletionCreateParams) -> None:
        response_format = params.get("response_format")
        if response_format is NOT_GIVEN:
            return

        json_schema_str, dataclasses_str, _ = try_convert_to_dataclasses_str(
            response_format
        )
        assert (
            dataclasses_str
        ), "The `response_format` parameter currently only supports subclasses of Pydantic BaseModel or input JSON schema!"

        json_schema = {
            "type": "json_schema",
            "json_schema": json.loads(json_schema_str),
        }
        params["response_format"] = json_schema
