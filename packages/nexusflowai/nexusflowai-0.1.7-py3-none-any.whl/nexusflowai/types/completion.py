from typing import List, Optional

from typing_extensions import Literal

from openai._models import BaseModel

from nexusflowai.types.completion_choice import NexusflowAICompletionChoice
from nexusflowai.types.completion_usage import NexusflowAICompletionUsage


__all__ = ["NexusflowAICompletion"]


class NexusflowAICompletion(BaseModel):
    id: str
    """A unique identifier for the completion."""

    choices: List[NexusflowAICompletionChoice]
    """The list of completion choices the model generated for the input prompt."""

    created: int
    """The Unix timestamp (in seconds) of when the completion was created."""

    model: str
    """The model used for completion."""

    object: Literal["text_completion"]
    """The object type, which is always "text_completion" """

    system_fingerprint: Optional[str] = None
    """This fingerprint represents the backend configuration that the model runs with.

    Can be used in conjunction with the `seed` request parameter to understand when
    backend changes have been made that might impact determinism.
    """

    usage: Optional[NexusflowAICompletionUsage] = None
    """Usage statistics for the completion request."""

    class Config:
        """Override the base pydantic model behavior and raise exception if additional arguments are passed in the constructor"""

        extra = "forbid"
