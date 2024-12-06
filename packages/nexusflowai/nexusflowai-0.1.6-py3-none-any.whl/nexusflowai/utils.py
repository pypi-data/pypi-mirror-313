from typing import Dict, Any, Union, Literal

from openai._types import Headers

ALLOWED_MODELS = Literal["nexus-tool-use-20240816"]
CLIENT_HEADER_KEY = "X-Client-ID"
CLIENT_NAME = "NexusflowAI"


def get_extra_header() -> Dict[str, Any]:
    return {CLIENT_HEADER_KEY: CLIENT_NAME}


def transform_client_header(extra_headers: Union[Headers, None]) -> Headers:
    if not extra_headers:
        return get_extra_header()

    return extra_headers | get_extra_header()
