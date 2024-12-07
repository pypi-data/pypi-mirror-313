from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from dataclasses import asdict, dataclass

from itertools import chain, repeat

import json

import ast

from uuid import uuid4

from openai.types.chat import ChatCompletionToolParam
from openai.types.chat.completion_create_params import ResponseFormat
from openai.types.chat.chat_completion_tool_choice_option_param import (
    ChatCompletionNamedToolChoiceParam,
)

from nexusflowai.types import NexusflowAIChatCompletionMessageToolCall
from nexusflowai.types.chat_completion_message_tool_call import (
    Function as ChatCompletionFunctionCall,
)

from nexusflowai.validators.create_with_tools.utils import (
    CodeExecutionHelper,
    CleanedFunction,
    get_tool_choice_prefix,
    clean_raw_response,
)
from nexusflowai.validators.create_with_tools.preprocess import (
    RavenFunctionCall,
)
from nexusflowai.validators.json_schema_to_dataclasses import (
    try_convert_to_dataclasses_str,
)


def _collect_factory(
    fun_name: str,
    fun_calls: List[RavenFunctionCall],
    fun_args: Union[Dict[str, Any], None],
    fun_par_idx: int,
    par_fun_calls: List[List[RavenFunctionCall]],
) -> Callable:
    def _collect(*args, **kwargs) -> RavenFunctionCall:
        if fun_args is not None:
            fun_args_dict = fun_args.copy()
            new_kwargs = dict()

            for arg_key, arg in chain(zip(repeat(None), args), kwargs.items()):
                # First case: we encountered either a positional arg (i.e. arg_key is None), or a hallucinated keyword arg.
                if arg_key not in fun_args_dict:
                    # If this is an "extraneous" argument, i.e. all known fun params have already been matched to args, then just silently drop the arg.
                    if len(fun_args_dict) <= 0:
                        continue

                    # Clobber non-hallucinated arg keyword names that occur after the hallucinated arg.
                    new_arg_key = next(iter(fun_args_dict))

                # Second case: this is a keyword that matches one of the known params given in the fun def.
                else:
                    new_arg_key = arg_key

                new_kwargs[new_arg_key] = arg
                fun_args_dict.pop(new_arg_key)

            # Any remaining missing required params should be added as keyword args set to their "default" values.
            new_kwargs |= {
                arg_name: arg_dict["def"]
                for arg_name, arg_dict in fun_args_dict.items()
                if arg_dict["req"]
            }

            kwargs = new_kwargs

        elif args:
            raise TypeError("Positional args are not allowed in Raven function calls")

        fun_call = RavenFunctionCall(fun_name, kwargs)

        fun_calls.append(fun_call)

        while fun_par_idx >= len(par_fun_calls):
            par_fun_calls.append([])
        par_fun_calls[fun_par_idx].append(fun_call)

        return fun_call

    return _collect


@dataclass
class RavenFunctionNameVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.fun_names = []
        self.fun_par_idxs = []
        self.par_idx = 0

    def visit_Module(self, node: ast.Module) -> None:
        for sub_node in node.body:
            self.visit(sub_node)
            self.par_idx += 1

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name):
            self.fun_names.append(node.func.id)
            self.fun_par_idxs.append(self.par_idx)
        self.generic_visit(node)


class FunctionCallResponseTranslator:
    def get_function_names(self, tree: ast.AST) -> Tuple[List[str], List[int]]:
        fun_name_visitor = RavenFunctionNameVisitor()
        fun_name_visitor.visit(tree)
        return fun_name_visitor.fun_names, fun_name_visitor.fun_par_idxs

    def raw_response_to_tool_calls(
        self,
        tools: List[ChatCompletionToolParam],
        raw_response: str,
        tool_choice: ChatCompletionNamedToolChoiceParam | None = None,
    ) -> List[NexusflowAIChatCompletionMessageToolCall]:
        cfs = list(map(CleanedFunction.from_tool_param, tools))

        dirty_function_name_to_cf = {cf.dirty_name: cf for cf in cfs}
        tool_choice_prefix = get_tool_choice_prefix(
            tool_choice, dirty_function_name_to_cf
        )
        if tool_choice_prefix is not None:
            raw_response = f"{tool_choice_prefix}{raw_response}"

        clean_function_name_to_cf = {cf.clean_name: cf for cf in cfs}
        tools = [cf.clean_tool_param(tool) for cf, tool in zip(cfs, tools)]

        fun_name_to_args = self.maybe_parse_fun_args(tools)
        response = clean_raw_response(raw_response)
        fun_calls, par_fun_calls = self.parse_function_calls(response, fun_name_to_args)
        if not fun_calls:
            return []

        tool_calls = []
        for fun_calls in par_fun_calls:  # pylint: disable=redefined-argument-from-local
            if len(fun_calls) <= 0:
                continue

            fun_call = fun_calls[0]

            cf = clean_function_name_to_cf.get(fun_call.name)
            name, kwargs = fun_call.name, fun_call.kwargs
            if cf is not None:
                name, kwargs = cf.dirty_function_call_dict(name, kwargs)

            chat_fc = {"name": name}
            try:
                chat_fc["arguments"] = json.dumps(kwargs)
            except Exception as e:
                raise e

            tool_call = NexusflowAIChatCompletionMessageToolCall(
                id=f"call_{str(uuid4()).replace('-', '')}",
                type="function",
                function=ChatCompletionFunctionCall.model_validate(chat_fc),
                execution_result=None,
            )
            tool_calls.append(tool_call)

        return tool_calls

    def maybe_parse_fun_args(
        self, tools: List[ChatCompletionToolParam]
    ) -> Dict[str, Any]:
        fun_name_to_args = dict()

        for tool in tools:
            fun = tool["function"]
            fun_name = fun["name"]

            req_arg_names = set(fun["parameters"].get("required", []))

            args = {
                arg_name: {
                    "req": arg_name in req_arg_names,
                    "def": arg_dict.get("default", None),
                }
                for arg_name, arg_dict in fun["parameters"]
                .get("properties", dict())
                .items()
            }

            fun_name_to_args[fun_name] = args

        return fun_name_to_args

    def parse_function_calls(
        self, source: str, fun_name_to_args: Dict[str, Dict[str, Any]]
    ) -> Tuple[List[RavenFunctionCall], List[List[RavenFunctionCall]]]:
        fun_calls = []
        par_fun_calls = []

        ceh = CodeExecutionHelper()
        root_source, tree = ceh.clean_input(source)
        if tree is None:
            return fun_calls, par_fun_calls

        ceh.check_security(tree)

        fun_names, fun_par_idxs = self.get_function_names(tree)

        root_tree = ast.parse(root_source)
        for par_idx, tree in enumerate(root_tree.body):
            env = dict()
            for fun_name, fun_par_idx in zip(fun_names, fun_par_idxs):
                if par_idx != fun_par_idx:
                    continue

                fun_args = fun_name_to_args.get(fun_name, None)
                if fun_args is not None:
                    env[fun_name] = _collect_factory(
                        fun_name, fun_calls, fun_args, fun_par_idx, par_fun_calls
                    )
                else:
                    env[fun_name] = lambda *args, **kwargs: None

            source = ast.unparse(tree)

            try:
                exec(source, env)  # pylint: disable=exec-used
            except:  # pylint: disable=bare-except
                pass

        return fun_calls, par_fun_calls


class ResponseFormatTranslator:
    def raw_response_to_parsed(
        self,
        response_format: ResponseFormat,
        raw_response: str,
    ) -> Optional[Dict[str, Any]]:
        raw_response = clean_raw_response(raw_response)

        ceh = CodeExecutionHelper()
        raw_response, tree = ceh.clean_input(raw_response)
        if tree is None:
            return None

        ceh.check_security(tree)

        _, dataclasses_str, parser_results = try_convert_to_dataclasses_str(
            response_format, with_import=True
        )

        model_response = raw_response.removeprefix("extract_item(value=").removesuffix(
            ")"
        )

        context = dict()
        try:
            # pylint: disable=exec-used
            exec(dataclasses_str, context)
        except:
            # pylint: disable=raise-missing-from
            raise RuntimeError("Failed to parse dataclasses_str")

        try:
            # pylint: disable=eval-used
            python_res = eval(model_response, context)
        except:
            # pylint: disable=raise-missing-from
            raise RuntimeError("Failed to parse model response")

        json_res = asdict(python_res)

        aliases = {}
        for parser_result in parser_results:
            for field in parser_result.fields:
                if field.alias:
                    aliases[field.name] = field.alias
        self._replace_field_names(json_res, aliases)

        return json_res

    def _replace_field_names(self, obj: Any, aliases: Dict[str, str]) -> None:
        if not aliases:
            return

        if isinstance(obj, dict):
            for k in list(obj):
                self._replace_field_names(obj[k], aliases)
                if k in aliases:
                    obj[aliases[k]] = obj.pop(k)
        elif isinstance(obj, list):
            for obj_i in obj:
                self._replace_field_names(obj_i, aliases)
