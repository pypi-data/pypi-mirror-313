from typing import Optional

from typing_extensions import Literal

from openai._models import BaseModel
from openai.types.completion_choice import Logprobs

from nexusflowai.types.chat_completion_message import NexusflowAIChatCompletionMessage


__all__ = ["NexusflowAICompletionChoice"]


class NexusflowAICompletionChoice(BaseModel):
    finish_reason: Literal["stop", "length", "content_filter", "tool_calls"]
    """The reason the model stopped generating tokens.

    This will be `stop` if the model hit a natural stop point or a provided stop
    sequence, `length` if the maximum number of tokens specified in the request was
    reached, `content_filter` if content was omitted due to a flag from our
    content filters, or `tool_calls` if the model hit a tool call return.
    """

    index: int

    logprobs: Optional[Logprobs]

    text: str

    message: NexusflowAIChatCompletionMessage = None
    """The message returned by the model"""

    class Config:
        """Override the base pydantic model behavior and raise exception if additional arguments are passed in the constructor"""

        extra = "forbid"
