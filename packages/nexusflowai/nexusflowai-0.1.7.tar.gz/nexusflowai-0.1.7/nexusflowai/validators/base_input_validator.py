from dataclasses import dataclass

from typing import Optional, Type, Any, Union

from openai._types import NOT_GIVEN
from openai.types.chat.completion_create_params import (
    CompletionCreateParams as ChatCompletionCreateParams,
)
from openai.types.completion_create_params import CompletionCreateParams

BOT_END = "<bot_end>"
MAX_STOP_SEQUENCES = 4


@dataclass
class BaseInputValidator:
    request_body: Union[ChatCompletionCreateParams, CompletionCreateParams]

    def validate(self):
        raise NotImplementedError

    @classmethod
    def _validate_stop_token(
        cls, params: Union[ChatCompletionCreateParams, CompletionCreateParams]
    ):
        stop = params["stop"]
        if stop is NOT_GIVEN:
            stop = [BOT_END]
        elif isinstance(stop, str):
            stop = [stop, BOT_END] if stop != BOT_END else [BOT_END]
        elif isinstance(stop, list):
            if BOT_END not in stop:
                if len(stop) < MAX_STOP_SEQUENCES:
                    stop.append(BOT_END)
                else:
                    raise ValueError(
                        f"A maximum of {MAX_STOP_SEQUENCES} stop sequences can be used, and one of them should be {BOT_END}"
                    )
            elif len(stop) >= MAX_STOP_SEQUENCES:
                raise ValueError(
                    f"A maximum of {MAX_STOP_SEQUENCES} stop sequences can be used"
                )
        else:
            raise TypeError("Expected stop to be of type 'str' or 'list'")

        params["stop"] = stop

    @classmethod
    def _validate_stream(  # pylint: disable=unused-argument
        cls, params: Union[ChatCompletionCreateParams, CompletionCreateParams]
    ):
        return

    @classmethod
    def _validate_temperature(
        cls, params: Union[ChatCompletionCreateParams, CompletionCreateParams]
    ):
        if params.get("temperature") is NOT_GIVEN:
            params["temperature"] = 0.0

    @classmethod
    def _check_for_unsupported_parameter_value(
        cls,
        params: Union[ChatCompletionCreateParams, CompletionCreateParams],
        parameter_name: str,
        exception_class: Type[BaseException],
        supported_value: Optional[Any] = None,
        assign_supported_value: bool = False,
        exception_message: Optional[str] = None,
    ):
        """Raise an exception if the value of a parameter is not supported."""

        parameter_value = params.get(parameter_name)
        if parameter_value is NOT_GIVEN:
            if assign_supported_value:
                params[parameter_name] = supported_value
            return

        supported_value_present = supported_value is not None
        if supported_value_present and parameter_value == supported_value:
            return

        if exception_message is not None:
            message = exception_message
        elif supported_value_present:
            message = (
                f"The only supported value for the {parameter_name} parameter is "
                f"{supported_value}"
            )
        else:
            message = f"The {parameter_name} parameter is not supported"

        raise exception_class(message)
