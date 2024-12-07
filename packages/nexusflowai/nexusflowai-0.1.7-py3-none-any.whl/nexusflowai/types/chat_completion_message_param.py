from typing import Union
from typing_extensions import TypeAlias

from openai.types.chat import (
    ChatCompletionToolMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionFunctionMessageParam,
)

from nexusflowai.types.chat_completion_assistant_message_param import (
    NexusflowAIChatCompletionAssistantMessageParam,
)

NexusflowAIChatCompletionMessageParam: TypeAlias = Union[
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    NexusflowAIChatCompletionAssistantMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionFunctionMessageParam,
]
