from typing import Union, Optional, Iterable
from typing_extensions import Literal, Required

from openai.types.chat.completion_create_params import CompletionCreateParamsBase

from nexusflowai.types.chat_completion_message_param import (
    NexusflowAIChatCompletionMessageParam,
)


class NexusflowAICompletionCreateParamsBase(CompletionCreateParamsBase):
    messages: Required[Iterable[NexusflowAIChatCompletionMessageParam]]


class NexusflowAICompletionCreateParamsNonStreaming(
    CompletionCreateParamsBase, total=False
):
    stream: Optional[Literal[False]]


class NexusflowAICompletionCreateParamsStreaming(CompletionCreateParamsBase):
    stream: Required[Literal[True]]


NexusflowAICompletionCreateParams = Union[
    NexusflowAICompletionCreateParamsNonStreaming,
    NexusflowAICompletionCreateParamsStreaming,
]
