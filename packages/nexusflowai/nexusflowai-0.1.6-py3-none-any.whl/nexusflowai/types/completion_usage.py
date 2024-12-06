from typing import Optional

from openai._models import BaseModel

__all__ = ["NexusflowAICompletionUsage"]


class NexusflowAICompletionUsage(BaseModel):
    completion_tokens: int
    """Number of tokens in the generated completion."""

    prompt_tokens: int
    """Number of tokens in the prompt."""

    total_tokens: int
    """Total number of tokens used in the request (prompt + completion)."""

    latency: Optional[float] = None
    """Time taken for this request in ms. Optional to retain compatibility with OpenAI responses."""

    time_to_first_token: Optional[float] = None
    """Time until the first token was generated in ms. Only returned for streamed requests."""

    output_tokens_per_sec: Optional[float] = None
    """Output tokens per second. Only returned for streamed requests."""
