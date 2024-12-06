from typing import Any, Dict, List, Optional, Type, Union

from dataclasses import dataclass

from collections import Counter

from copy import deepcopy

import json
from json import JSONDecodeError

import json_repair

from openai.types.chat import ChatCompletionMessageToolCallParam
from openai.types.chat.completion_create_params import (
    CompletionCreateParams as ChatCompletionCreateParams,
    ChatCompletionMessageParam,
)

from nexusflowai.validators.json_schema_to_dataclasses import (
    try_convert_to_dataclasses_str,
)
from nexusflowai.validators.create_with_tools.utils import (
    ALLOWED_ROLES,
    CleanedFunction,
    get_tool_choice_prefix,
    _parse_content_parts,
)


@dataclass
class RavenType:
    TYPE_KEY = "type"

    schema: Any

    @classmethod
    def format_type_for_prompt(
        cls,
        parameter_type: Union[str, List[Any]],
        parameter_schema: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """Format the specified parameter (or return) type.

        Return a string representation of the specified parameter type that is to
        be used in a prompt.
        """

        if isinstance(parameter_type, list):
            alternative_types = Counter()
            for type_name in parameter_type:
                if not isinstance(type_name, str):
                    continue

                alternative_type = cls.format_type_for_prompt(type_name)
                if alternative_type is not None:
                    alternative_types[alternative_type] += 1

            num_alternative_types = len(alternative_types)
            if num_alternative_types > 1:
                types_string = ", ".join(alternative_types)
                return f"Union[{types_string}]"
            elif num_alternative_types == 1:
                return next(iter(alternative_types))
            else:
                return None

        if parameter_type == "string":
            return "str"

        if parameter_type == "number":
            return "float"

        if parameter_type == "integer":
            return "int"

        # pylint: disable=too-many-nested-blocks
        if parameter_type == "object":
            # In principle, a type could be assigned to the values in a
            # dictionary based on the types of the properties of the object.
            # However, this could be complicated by the possibility that there
            # could be additional properties in an object that are not
            # specified in the properties.  For now, no types are provided for
            # the keys and values in the dictionary for simplicity.

            # "Dict" for (nested) dict.
            if parameter_schema is not None:
                properties = parameter_schema.get("properties")
                if isinstance(properties, dict):
                    for _prop_key, prop_value in properties.items():
                        if not isinstance(prop_value, dict):
                            continue
                        element_type = prop_value.get(cls.TYPE_KEY)
                        if isinstance(element_type, (str, list)):
                            prompt_element_type = cls.format_type_for_prompt(
                                element_type, parameter_schema=prop_value
                            )
                            if prompt_element_type is not None:
                                return f"Dict[str, {prompt_element_type}]"
                    return "Dict"

                extra_properties = parameter_schema.get("additionalProperties")
                if isinstance(extra_properties, dict):
                    element_type = extra_properties.get(cls.TYPE_KEY)
                    if isinstance(element_type, (str, list)):
                        prompt_element_type = cls.format_type_for_prompt(
                            element_type, parameter_schema=extra_properties
                        )
                        if prompt_element_type is not None:
                            return f"Dict[str, {prompt_element_type}]"
                    return "Dict"

            # Otherwise, prefer "object" instead of "dict".
            return "object"

        if parameter_type == "array":
            if parameter_schema is not None:
                array_items = parameter_schema.get("items")
                if isinstance(array_items, dict):
                    element_type = array_items.get(cls.TYPE_KEY)
                    if isinstance(element_type, (str, list)):
                        prompt_element_type = cls.format_type_for_prompt(
                            element_type, parameter_schema=array_items
                        )
                        if prompt_element_type is not None:
                            return f"List[{prompt_element_type}]"

            return "list"

        if parameter_type == "boolean":
            return "bool"

        if parameter_type == "null":
            return "None"

        return None


@dataclass
class RavenFunctionReturn(RavenType):
    """This class represents a function return type."""

    def format_for_prompt_definition(self) -> Union[str, None]:
        """Format this function return type.

        Return a string representation of this function return type that is to be
        part of the function definition of a prompt.
        """

        if not isinstance(self.schema, dict):
            return None

        parameter_type = self.schema.get(self.TYPE_KEY)
        if not isinstance(parameter_type, (str, list)):
            return None

        prompt_type = self.format_type_for_prompt(
            parameter_type, parameter_schema=self.schema
        )
        if not prompt_type:
            return None
        else:
            return f"{prompt_type}"


@dataclass
class RavenFunctionParameter(RavenType):
    """This class represents a parameter in a function definition."""

    DESC_KEY = "description"

    name: str
    required: bool = True

    def format_for_prompt_docstring(self) -> Union[str, None]:
        """Format this function parameter.

        Return a string representation of this function parameter that is to be
        described in the function docstring of a prompt.
        """

        if not isinstance(self.schema, dict):
            return None

        parameter_desc = self.schema.get(self.DESC_KEY)
        if isinstance(parameter_desc, str):
            parameter_desc = parameter_desc.strip()
        else:
            if "items" in self.schema and "description" in self.schema["items"]:
                parameter_desc = self.schema["items"]["description"]
                if isinstance(parameter_desc, str):
                    parameter_desc = parameter_desc.strip()
                else:
                    parameter_desc = ""
            else:
                parameter_desc = ""
        if parameter_desc:
            # Parameter description begins with upper case.
            parameter_desc = f"{parameter_desc[0].upper()}{parameter_desc[1:]}"

        parameter_type = self.schema.get(self.TYPE_KEY)
        if not isinstance(parameter_type, (str, list)):
            return None

        prompt_type = self.format_type_for_prompt(
            parameter_type, parameter_schema=self.schema
        )

        desc_parts = [parameter_desc.strip()]

        # Parameter descriptions end with a dot.
        if desc_parts[0] and not desc_parts[0].endswith("."):
            desc_parts.append(".")

        # "robustly" handling default values.
        if "default" in self.schema:
            default = self.schema.get("default")
            if default is not None and parameter_type is not None:
                parameter_cls_name = self.format_type_for_prompt(parameter_type, None)
                parameter_cls = eval(parameter_cls_name)  # pylint: disable=eval-used
                if not (parameter_cls is object or issubclass(parameter_cls, str)):
                    try:
                        if isinstance(default, str):
                            default = parameter_cls(json.loads(default))
                        else:
                            default = parameter_cls(default)
                    except Exception:  # pylint: disable=broad-exception-caught
                        if default == "None":
                            default = None
            desc_parts.append(f" Default value: {repr(default)}.")
        elif not self.required:
            # Sometimes the description specifies a default value using natural language
            # but that same default value does not occur in the schema.
            default = None
            desc_parts.append(f" Default value: {repr(default)}.")

        # Optional parameters.
        if not self.required:
            desc_parts.append(" (Optional)")

        # Nested dicts.
        if "properties" in self.schema and isinstance(self.schema["properties"], dict):
            desc_parts.append(" Has keys:")
            some_prop_doc = False
            for prop_key, prop_value in self.schema["properties"].items():
                prop_type = prop_value.get(self.TYPE_KEY)
                if not isinstance(prop_type, str):
                    continue
                some_prop_doc = True
                prop_prompt_type = self.format_type_for_prompt(
                    prop_type, parameter_schema=prop_value
                )
                prop_desc = prop_value.get(self.DESC_KEY)
                if isinstance(prop_desc, str):
                    prop_desc = prop_desc.strip()
                if not prop_prompt_type:
                    if not prop_desc:
                        desc_parts.append(f"\n    - {prop_key}")
                    else:
                        desc_parts.append(f"\n    - {prop_key}: {prop_desc}")
                else:
                    if not prop_desc:
                        desc_parts.append(f"\n    - {prop_key} ({prop_prompt_type})")
                    else:
                        desc_parts.append(
                            f"\n    - {prop_key} ({prop_prompt_type}): {prop_desc}"
                        )
            if not some_prop_doc:
                desc_parts.append("\n")

        # Not duplicating enum lists in parameter description.
        min_enum_occur_ct = 3
        if "enum" in self.schema and isinstance(self.schema["enum"], list):
            occur_ct = 0
            for value in self.schema["enum"]:
                if parameter_desc.find(value) >= 0:
                    occur_ct += 1
                    if occur_ct >= min(min_enum_occur_ct, len(self.schema["enum"])):
                        break
            if not occur_ct >= min(min_enum_occur_ct, len(self.schema["enum"])):
                desc_parts.append(" Available values:")
                for value in self.schema["enum"]:
                    desc_parts.append(f"\n    - {repr(value)}")
        elif (
            isinstance(prompt_type, str)
            and prompt_type.startswith("List[")
            and "enum" in self.schema["items"]
            and isinstance(self.schema["items"]["enum"], list)
        ):
            occur_ct = 0
            for value in self.schema["items"]["enum"]:
                if parameter_desc.find(value) >= 0:
                    occur_ct += 1
                    if occur_ct >= min(
                        min_enum_occur_ct, len(self.schema["items"]["enum"])
                    ):
                        break
            if not (
                occur_ct >= min(min_enum_occur_ct, len(self.schema["items"]["enum"]))
            ):
                desc_parts.append(" Available entries:")
                for value in self.schema["items"]["enum"]:
                    desc_parts.append(f"\n    - {repr(value)}")

        parameter_desc = "".join(desc_parts)

        if not prompt_type:
            if not parameter_desc:
                return f"- {self.name}"
            else:
                return f"- {self.name}: {parameter_desc}"
        else:
            if not parameter_desc:
                return f"- {self.name} ({prompt_type})"
            else:
                return f"- {self.name} ({prompt_type}): {parameter_desc}"

    def format_for_prompt_definition(self) -> str:
        """Format this function parameter.

        Return a string representation of this function parameter that is to be
        part of the function definition of a prompt.
        """

        if not isinstance(self.schema, dict):
            if self.required:
                return self.name
            else:
                default = None
                return f"{self.name}={repr(default)}"

        parameter_type = self.schema.get(self.TYPE_KEY)
        default = self.schema.get("default")

        # "robustly" handling default values.
        if "default" in self.schema:
            if default is not None and parameter_type is not None:
                parameter_cls_name = self.format_type_for_prompt(parameter_type, None)
                parameter_cls = eval(parameter_cls_name)  # pylint: disable=eval-used
                if not (parameter_cls is object or issubclass(parameter_cls, str)):
                    try:
                        if isinstance(default, str):
                            default = parameter_cls(json.loads(default))
                        else:
                            default = parameter_cls(default)
                    except Exception:  # pylint: disable=broad-exception-caught
                        if default == "None":
                            default = None

        if not isinstance(parameter_type, (str, list)):
            if self.required:
                return self.name
            else:
                return f"{self.name}={repr(default)}"

        prompt_type = self.format_type_for_prompt(
            parameter_type, parameter_schema=self.schema
        )
        # Required param with default value.
        if not prompt_type:
            if not self.required or "default" in self.schema:
                return f"{self.name}={repr(default)}"
            else:
                return self.name
        else:
            if not self.required or "default" in self.schema:
                return f"{self.name}: {prompt_type} = {repr(default)}"
            else:
                return f"{self.name}: {prompt_type}"


@dataclass
class RavenFunctionDefinition:
    """This class represents a function definition."""

    NEWLINE = "\n"
    DOCSTRING_INDENT = "    "
    DOCSTRING_TEMPLATE = '''{indent}"""
{indent}{description}"""
'''
    FUNCTION_TEMPLATE = """Function:
def {name}({parameters}){returns}:
{docstring}
"""

    name: str
    parameters: List[RavenFunctionParameter]  # non-standard "returns"
    returns: List[RavenFunctionReturn]
    description: Optional[str]  # non-standard "extra_description"
    extra_description: Optional[str] = None

    def format_for_prompt(self) -> str:
        """Format this function definition.

        Return a string representation of this function definition that is to be
        used in a prompt.
        """

        parameter_strings = [
            parameter.format_for_prompt_definition() for parameter in self.parameters
        ]
        combined_parameters = ", ".join(parameter_strings)

        if not self.returns:
            returns = ""
        else:
            returns = self.returns[0].format_for_prompt_definition()
            if returns is None:
                returns = ""
            else:
                returns = f" -> {returns}"

        if self.description is not None:
            desc_blocks = [self.description.strip()]
            for p in self.parameters:
                d = p.format_for_prompt_docstring()
                if d is not None:
                    if len(desc_blocks) <= 1:
                        desc_blocks.append("")
                        desc_blocks.append("Parameters:")
                    desc_blocks.append(d)
            if self.extra_description is not None:
                desc_blocks.append("")
                desc_blocks.append(self.extra_description.strip())
            formatted_lines = []
            formatted_lines.append(f'{self.DOCSTRING_INDENT}"""')
            for block in desc_blocks:
                if block:
                    for line in block.splitlines():
                        formatted_lines.append(f"{self.DOCSTRING_INDENT}{line}")
                else:
                    formatted_lines.append("")
            formatted_lines.append(f'{self.DOCSTRING_INDENT}"""')
            formatted_lines.append("")
            docstring = self.NEWLINE.join(formatted_lines)
        else:
            docstring = ""

        return self.FUNCTION_TEMPLATE.format(
            name=self.name,
            parameters=combined_parameters,
            returns=returns,
            docstring=docstring,
        )


@dataclass
class RavenFunctionCall:
    name: str
    kwargs: Dict[str, Any]

    def __repr__(self) -> str:
        kwargs_repr = ", ".join(f"{k}={repr(v)}" for k, v in self.kwargs.items())
        return f"{self.name}({kwargs_repr})"

    @classmethod
    def from_tool_call(cls, tool_call: Dict[str, Any]) -> "RavenFunctionCall":
        function_name = tool_call["function"]["name"]
        function_kwargs = json_repair.loads(tool_call["function"]["arguments"])
        return cls(
            name=function_name,
            kwargs=function_kwargs,
        )


@dataclass
class RavenQuery:
    """This class represents a query that is to be sent to the Raven model."""

    PROMPT_TEMPLATE = (
        "{functions}{response_format}{system_query}{turns}{tool_choice_prefix}"
    )
    HUMAN_END_SUFFIX = " <human_end>\n\nCall:"

    functions: List[RavenFunctionDefinition]
    response_format: str
    system_query: str
    messages: List[Any]
    tool_choice_prefix: str | None

    def construct_prompt(self) -> str:
        """Return the prompt for the Raven model for this query."""

        function_strings = [function.format_for_prompt() for function in self.functions]
        combined_functions = "".join(function_strings)

        response_format = self.response_format
        if self.response_format is None:
            response_format = ""
        elif isinstance(response_format, dict):
            _, dataclasses_str, _ = try_convert_to_dataclasses_str(response_format)
            """
            @dataclass
            class Person:
                name: str
                age: int
                email: Optional[str] = None
            """
            # pylint: disable=use-maxsplit-arg
            top_level_obj_cls = dataclasses_str.split("@dataclass\nclass ")[-1]
            top_level_obj_cls = top_level_obj_cls.split(":")[0]

            indent = RavenFunctionDefinition.DOCSTRING_INDENT
            response_format = f"""{dataclasses_str}
Function:
def extract_item(value: {top_level_obj_cls}): 
{indent}\"\"\"
{indent}Please extract the necessary information in the format requested using the data-classes above and pass them in.
{indent}\"\"\"

"""
            combined_functions = ""
        else:
            raise NotImplementedError("Unknown response format schema")

        turns = self.format_turns(self.messages)

        if self.system_query is None:
            system_query = ""
        else:
            system_query = self.system_query.strip()
            system_query = f"Instruction: {system_query}\n\n"

        tool_choice_prefix = ""
        if self.tool_choice_prefix is not None:
            tool_choice_prefix = f" {self.tool_choice_prefix}"

        return self.PROMPT_TEMPLATE.format(
            functions=combined_functions,
            response_format=response_format,
            system_query=system_query,
            turns=turns,
            tool_choice_prefix=tool_choice_prefix,
        )

    def format_turns(self, messages: List[ChatCompletionMessageParam]) -> str:
        user_query_idxs = [i for i, m in enumerate(messages) if m["role"] == "user"]

        non_user_query_idxs = [i for i, m in enumerate(messages) if m["role"] != "user"]
        shifted_queries = messages.copy()
        # Shift all non-user queries to come before user queries
        for idx in non_user_query_idxs:
            if idx != 0:
                shifted_queries[idx - 1], shifted_queries[idx] = (
                    shifted_queries[idx],
                    shifted_queries[idx - 1],
                )

        tool_call_id_to_result = dict()
        input_tool_param_ids = []
        for message in messages:
            if message["role"] != "tool":
                continue

            try:
                content = json.loads(message["content"])
            except JSONDecodeError:
                content = message["content"]

            tool_call_id_to_result[message["tool_call_id"]] = content

            input_tool_param_ids.append(message["tool_call_id"])

        input_tool_call_param_ids = []
        for message in messages:
            if message["role"] != "assistant":
                continue

            input_tool_call_param_ids.extend(
                [t["id"] for t in message.get("tool_calls") or []]
            )

        # We use lists here rather than sets to keep the order of the returns the same
        # as the order of the inputs. This is more intuitive to the user since there is an ordering.
        extra_tool_results = [
            i for i in input_tool_param_ids if i not in input_tool_call_param_ids
        ]
        assert not extra_tool_results, f"""ToolMessage / ToolCallParam mismatch! (extra ChatCompletionToolMessageParam `tool_call_id`s)
The following ChatCompletionToolMessageParam `tool_call_id`s don't have a corresponding ChatCompletionAssistantMessageParam ChatCompletionMessageToolCallParam `id`.
Extra ChatCompletionToolMessageParam `tool_call_id`s: {extra_tool_results}
Here are the ChatCompletionAssistantMessageParam ChatCompletionMessageToolCallParam `id`s that we found: {input_tool_call_param_ids}"""

        num_turns = len(user_query_idxs)

        res = ""
        is_new_turn = True
        is_new_assistant_turn = True
        turn = 1
        for message in shifted_queries:
            is_last_turn = turn == num_turns

            message_content = message.get("content", [])
            if message_content:
                if isinstance(message_content, List):
                    content_strs = _parse_content_parts(message_content)
                else:
                    content_strs = [message_content]
            else:
                content_strs = []

            if is_new_turn:
                if is_last_turn:
                    res += "Current Turn:\n"
                else:
                    res += f"Turn {turn}:\n"

            if message["role"] == "assistant":
                tool_calls = message.get("tool_calls") or []

                if is_new_assistant_turn:
                    # Chat Response
                    for content in content_strs:
                        if is_last_turn:
                            res += f"Original Plan: {content}\n"
                        else:
                            res += f"Previous Original Plan: {content}\n"

                    # Planning
                    previous_original_plan = json.loads(
                        message.get("nexusflowai_extras", "{}")
                    ).get("original_plan")
                    if previous_original_plan is not None:
                        if is_last_turn:
                            res += f"Original Plan: {previous_original_plan}\n"
                        else:
                            res += f"Previous Original Plan: {previous_original_plan}\n"

                for tool_call in tool_calls:
                    tool_call_id = tool_call["id"]
                    if tool_call_id not in tool_call_id_to_result:
                        continue

                    previous_call = RavenFunctionCall.from_tool_call(tool_call)
                    previous_result = tool_call_id_to_result.pop(tool_call_id)

                    res += f"""Previous Call: {previous_call}
Previous Result: {previous_result}
"""
                is_new_turn = False
                is_new_assistant_turn = False

            elif message["role"] == "user":
                if is_last_turn:
                    res += self._format_final_user_query(content_strs)
                else:
                    for content in content_strs[:-1]:
                        res += f"Previous User Query: {content}\n"
                    res += f"Previous User Query: {content_strs[-1]} <turn_end>\n\n"

                turn += 1
                is_new_turn = True
                is_new_assistant_turn = True
            else:
                is_new_turn = False

        # Sometimes only system prompts are input
        if len(user_query_idxs) == 0:
            res += self.HUMAN_END_SUFFIX

        return res

    def _format_final_user_query(self, content_strs: List[str]) -> str:
        final_query_str = "\n".join(
            [f"User Query: {content}\n" for content in content_strs[:-1]]
        )
        final_query_str += f"User Query: {content_strs[-1]}{self.HUMAN_END_SUFFIX}"
        return final_query_str


class FunctionCallTranslator:
    RETURNS_KEY = "returns"  # Non-standard "returns".
    EXTRA_DESCRIPTION_KEY = "extra_description"  # Non-standard "extra_description".

    RAVEN_QUERY_CLS: Type[RavenQuery] = RavenQuery

    def get_raven_func_definitions(
        self, tools: List[Dict[str, Any]]
    ) -> List[RavenFunctionDefinition]:
        functions = []
        for tool in tools:
            tool_function = tool["function"]
            function_name = tool_function["name"]
            function_parameters = tool_function["parameters"]

            defined_parameters = []
            required_parameters = set(function_parameters.get("required", []))
            function_properties = function_parameters.get("properties", {})
            for parameter_name, parameter_schema in function_properties.items():
                defined_parameter = RavenFunctionParameter(
                    name=parameter_name,
                    schema=parameter_schema,
                    required=parameter_name in required_parameters,
                )
                defined_parameters.append(defined_parameter)

            if self.RETURNS_KEY not in tool_function:
                function_returns = []
            else:
                function_returns = [
                    RavenFunctionReturn(schema=tool_function[self.RETURNS_KEY])
                ]

            function_description = tool_function.get("description")

            function_extra_description = tool_function.get(self.EXTRA_DESCRIPTION_KEY)

            function_definition = RavenFunctionDefinition(
                name=function_name,
                parameters=defined_parameters,
                returns=function_returns,
                description=function_description,
                extra_description=function_extra_description,
            )
            functions.append(function_definition)

        return functions

    def create_params_to_fc_prompt(
        self, create_params: ChatCompletionCreateParams
    ) -> str:
        messages = create_params["messages"]

        for message in messages:
            role = message["role"]
            assert (
                role in ALLOWED_ROLES
            ), f"The `{role}` role is not supported. Supported roles: {repr(ALLOWED_ROLES)}"

        system_queries = []
        for message in messages:
            if message["role"] != "system":
                continue

            system_query = message["content"]
            if isinstance(system_query, List):
                content_strs = _parse_content_parts(system_query)
                system_query = "\n".join(content_strs)
            system_queries.append(system_query)

        system_query = "\n".join(system_queries)
        system_query = system_query or None

        tools = create_params.get("tools") or []
        cfs = list(map(CleanedFunction.from_tool_param, tools))
        dirty_function_name_to_cf = {cf.dirty_name: cf for cf in cfs}
        tool_choice_prefix = get_tool_choice_prefix(
            create_params.get("tool_choice"), dirty_function_name_to_cf
        )
        tools = [cf.clean_tool_param(tool) for cf, tool in zip(cfs, tools)]

        messages = deepcopy(messages)
        for message in messages:
            if message["role"] != "assistant":
                continue

            tool_calls = message.get("tool_calls")
            if not tool_calls:
                continue

            clean_tool_calls = []
            for dirty_tool_call in tool_calls:
                dirty_tool_call: ChatCompletionMessageToolCallParam

                cf = dirty_function_name_to_cf.get(dirty_tool_call["function"]["name"])
                if cf is None:
                    clean_tool_calls.append(dirty_tool_call)
                else:
                    clean_tool_call = cf.clean_tool_call_param(dirty_tool_call)
                    clean_tool_calls.append(clean_tool_call)

            message["tool_calls"] = clean_tool_calls

        functions = self.get_raven_func_definitions(tools)

        response_format = create_params.get("response_format")

        query = self.RAVEN_QUERY_CLS(
            functions=functions,
            response_format=response_format,
            system_query=system_query,
            messages=messages,
            tool_choice_prefix=tool_choice_prefix,
        )
        return query.construct_prompt()
