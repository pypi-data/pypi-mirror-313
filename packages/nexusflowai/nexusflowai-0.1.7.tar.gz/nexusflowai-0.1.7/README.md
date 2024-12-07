# NexusflowAI Python API library

[![PyPI version](https://img.shields.io/pypi/v/nexusflowai?pypiBaseUrl=https://pypi.org)](https://pypi.org/project/nexusflowai/)

Welcome to the NexusflowAI API by [Nexusflow.ai](https://nexusflow.ai/)!

```bash
pip install nexusflowai
```

This package is based on and extends from the [OpenAI Python Library](https://github.com/openai/openai-python). Cheers to the OpenAI team for an amazing API library and SDK!


# Usage
## Completions
```python
from nexusflowai import NexusflowAI


nf = NexusflowAI(api_key="<api key>")


response = nf.completions.create(
    model="nexus-tool-use-20240816",
    prompt="""Function:
def get_weather(city_name: str):
\"\"\"
\"\"\"


User Query: i am in berkeley.<human_end>Call:""",
    stop=["<bot_end>"],
    max_tokens=10,
)
print(response)
```

## ChatCompletions with Tools
```python
from nexusflowai import NexusflowAI


nf = NexusflowAI(api_key="<api key>")


response = nf.chat.completions.create(
    model="nexus-tool-use-20240816",
    messages=[
        {
            "role": "user",
            "content": "i am in berkeley.",
        },
    ],
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city_name": {
                            "type": "string",
                            "description": "",
                        },
                    },
                    "required": ["city_name"],
                    "additionalProperties": False,
                }
            }
        }
    ],
)
print(response)
```

## Multiturn ChatCompletions with Tools + Planning
For Multiturn Chat Completions with Planning, you must use the "nexusflowai_extras" message parameter returned with the chat completion in the previous response.

To do so, simply append the message output of the previous chat completion call to the conversation history.

Example:
```python
from nexusflowai import NexusflowAI


nf = NexusflowAI(api_key="<api key>")

tools_list = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "returns True if weather is nice, False otherwise",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "call_taxi",
            "description": "",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            }
        }
    }
]

# Setup Initial Message
messages_list = [
    {
        "role": "user",
        "content": "Get the weather, and then call a taxi.",
    },
]

response = nf.chat.completions.create(
    model="nexus-tool-use-20240816",
    messages=messages_list,
    tools=tools_list
)

print(response.model_dump_json(indent=4))
"""
Output contains `nexusflowai_extras` field in the chat.completion.choices.messages parameter.

output:
{
    "id": "44d060af-ae7c-4166-a3ab-2937231bb126",
    "choices": [
        {
            "finish_reason": "tool_calls",
            "index": 0,
            "message": {
                "content": null,
                "refusal": null,
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": "call_de128c8884e24a0aba92ae88ea40852b",
                        "function": {
                            "arguments": "{}",
                            "name": "get_weather"
                        },
                        "type": "function",
                        "execution_result": null
                    },
                    {
                        "id": "call_e9cbc49b5bdd477da7c2db3deb0d7709",
                        "function": {
                            "arguments": "{}",
                            "name": "call_taxi"
                        },
                        "type": "function",
                        "execution_result": null
                    }
                ],
                "parsed": null,
                "nexusflowai_extras": "{\"original_plan\": \"get_weather(); call_taxi()\"}"
            }
        }
    ],
    "created": 1733280031,
    "model": "nexus-tool-use-20240816",
    "object": "chat.completion",
    "system_fingerprint": null,
    "usage": {
        "completion_tokens": 8,
        "prompt_tokens": 54,
        "total_tokens": 62,
        "latency": 0.35005688667297363,
        "time_to_first_token": null,
        "output_tokens_per_sec": null
    },
    "hints": null
}
"""

# Add previous assistant message with the `nexusflowai_extras` field to messages
messages_list.append(
    response.choices[0].message
)

response = nf.chat.completions.create(
    model="nexus-tool-use-20240816",
    messages=messages_list,
    tools=tools_list,
)

print(response.model_dump_json(indent=4))
"""
output:
{
    "id": "2bc46052-9951-475d-b0d6-6471207bdc90",
    "choices": [
        {
            "finish_reason": "tool_calls",
            "index": 0,
            "message": {
                "content": null,
                "refusal": null,
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": "call_fc412fc4f399449a88a5cce69d0635ab",
                        "function": {
                            "arguments": "{}",
                            "name": "call_taxi"
                        },
                        "type": "function",
                        "execution_result": null
                    }
                ],
                "parsed": null,
                "nexusflowai_extras": "{\"original_plan\": \"call_taxi()\"}"
            }
        }
    ],
    "created": 1733279748,
    "model": "nexus-tool-use-20240816",
    "object": "chat.completion",
    "system_fingerprint": null,
    "usage": {
        "completion_tokens": 5,
        "prompt_tokens": 61,
        "total_tokens": 66,
        "latency": 0.24212288856506348,
        "time_to_first_token": null,
        "output_tokens_per_sec": null
    },
    "hints": null
}
"""
```


## ChatCompletions with Structured Outputs
```python
from typing import List, Dict, Tuple

from pydantic import BaseModel, Field

from nexusflowai import NexusflowAI


nf = NexusflowAI(api_key="<api key>")


class GasDistributionNetwork(BaseModel):
    networkID: str = Field(
        ...,
        description="The identifier for the gas distribution network.",
        title="Network ID",
    )
    pipelineValues: Dict[str, Tuple[int, int]] = Field(
        description="The mapping with key pipeline_1, pipeline_2, etc ... to tuple of (total length in kilometers, maximum amount of gas that can be distributed in cubic meters).",
        title="Pipeline Values",
    )
    maintenanceSchedules: List[str] = Field(
        ...,
        description="The schedule detailing when maintenance activities are to be performed.",
        title="Maintenance Schedule",
    )


response = nf.chat.completions.create(
    model="nexus-tool-use-20240816",
    messages=[
        {
            "role": "user",
            "content": """I am currently working on a project that involves mapping out a gas distribution network for a new residential area. The network is quite extensive and includes several pipelines that distribute natural gas to various sectors of the community. I need to create a JSON object that captures the essential details of this network. The information I have includes a unique identifier for the network, which is 'GDN-4521'. The total length of the pipeline_1 is 275 kilometers with a capacity 500,000 cubic meters. Pipeline 2 is 17 kilometers long and has a capacity of 12,000 cubic meters. Additionally, there is a detailed maintenance schedule, which includes quarterly inspections in January, April, July, and October.""",
        },
    ],
    response_format=GasDistributionNetwork,
)
print(response.raw_prompt)
print(response.choices[0].message.parsed)
```
