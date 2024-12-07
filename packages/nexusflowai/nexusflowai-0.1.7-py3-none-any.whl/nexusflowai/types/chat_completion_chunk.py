from typing import List, Optional

from openai.types.chat.chat_completion_chunk import (
    ChatCompletionChunk as BaseChatCompletionChunk,
)

__all__ = ["NexusflowAIChatCompletionChunk"]


class NexusflowAIChatCompletionChunk(BaseChatCompletionChunk):
    hints: Optional[List[str]] = None
