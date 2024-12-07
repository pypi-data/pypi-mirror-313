from dataclasses import dataclass

from openai.types.completion_create_params import CompletionCreateParams
from nexusflowai.validators.base_input_validator import BaseInputValidator


@dataclass
class CompletionsInputValidator(BaseInputValidator):
    def validate(self) -> CompletionCreateParams:
        self._validate_stream(params=self.request_body)

        self._validate_stop_token(params=self.request_body)

        self._check_for_unsupported_parameter_value(
            params=self.request_body,
            parameter_name="best_of",
            exception_class=NotImplementedError,
            supported_value=1,
            assign_supported_value=True,
        )
        self._check_for_unsupported_parameter_value(
            params=self.request_body,
            parameter_name="echo",
            exception_class=NotImplementedError,
            supported_value=False,
            assign_supported_value=True,
        )
        self._check_for_unsupported_parameter_value(
            params=self.request_body,
            parameter_name="n",
            exception_class=NotImplementedError,
            supported_value=1,
            assign_supported_value=True,
        )

        self._check_for_unsupported_parameter_value(
            params=self.request_body,
            parameter_name="logprobs",
            exception_class=NotImplementedError,
            exception_message="Logprobs is not supported at this time",
        )

        self._validate_temperature(params=self.request_body)

        return self.request_body
