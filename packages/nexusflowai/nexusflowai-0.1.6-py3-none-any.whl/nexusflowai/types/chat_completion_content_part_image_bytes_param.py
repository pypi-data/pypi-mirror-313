from typing_extensions import Literal, Required, TypedDict

__all__ = ["NexusflowAIChatCompletionContentPartImageBytesParam"]


class NexusflowAIChatCompletionContentPartImageBytesParam(TypedDict, total=False):
    image_bytes: str
    """Base64 byte encoded image decoded as utf-8."""

    type: Required[Literal["image_bytes"]]
    """The type of the content part."""
