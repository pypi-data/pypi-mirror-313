from typing import Optional

from openai.types.chat import ChatCompletionAssistantMessageParam


class NexusflowAIChatCompletionAssistantMessageParam(
    ChatCompletionAssistantMessageParam
):
    nexusflow_extras: Optional[str] = None
    """Extra items passed in for Nexusflow client, formatted as a json string."""
