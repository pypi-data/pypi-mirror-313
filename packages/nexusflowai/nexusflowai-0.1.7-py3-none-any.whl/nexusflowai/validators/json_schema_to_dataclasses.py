from typing import Any, Dict, Optional, Tuple, Union

import json

from pydantic import BaseModel

from datamodel_code_generator.format import PythonVersion
from datamodel_code_generator.parser.jsonschema import JsonSchemaParser
from datamodel_code_generator.model import get_data_model_types

from datamodel_code_generator import DataModelType


def json_schema_to_dataclasses(
    json_schema: str, with_import: bool = False
) -> Optional[str]:
    target_python_version = PythonVersion.PY_38
    output_model_type = DataModelType.DataclassesDataclass
    data_model_types = get_data_model_types(output_model_type, target_python_version)

    parser = JsonSchemaParser(
        source=json_schema,
        data_model_type=data_model_types.data_model,
        data_model_root_type=data_model_types.root_model,
        data_model_field_type=data_model_types.field_model,
        data_type_manager_type=data_model_types.data_type_manager,
        use_schema_description=True,
        use_field_description=True,
    )

    try:
        results = parser.parse(with_import=with_import)
    except:  # pylint: disable=bare-except # pragma: no cover
        return None

    if not results:  # pragma: no cover
        return None
    elif isinstance(results, str):
        bodies = [results]
    else:
        bodies = [result.body for _, result in sorted(results.items())]

    parser_results = parser.results

    res = "\n\n".join(bodies)
    return res, parser_results


def try_convert_to_dataclasses_str(
    input_: Union[BaseModel, Dict[str, Any]], with_import: bool = False
) -> Tuple[Optional[str], Optional[str]]:
    """
    Returns
    -------
    json_schema_str: str
    dataclasses_str: str

    """
    if isinstance(input_, type) and issubclass(input_, BaseModel):
        input_: Dict[str, Any] = input_.model_json_schema()

    if not isinstance(input_, Dict):
        return None, None, None

    if input_.get("type") == "json_schema":
        json_schema = input_["json_schema"]
        # OpenAI strict style schema
        if "name" in json_schema:
            outer_name = input_["json_schema"]["name"]
            input_ = input_["json_schema"]["schema"]
            input_["title"] = outer_name
        else:  # NexusflowAI mimic format
            input_ = input_["json_schema"]

    is_object_type = input_.get("type") == "object"
    has_allOf = input_.get("allOf") is not None
    has_ref = input_.get("$ref") is not None
    assert (
        is_object_type or has_allOf or has_ref
    ), f"Input JSON schema top-level type must be an object, but got `{input_.get('type')}`"

    try:
        str_input_ = json.dumps(input_)
    except json.JSONDecodeError:  # pragma: no cover
        return None, None, None

    res, datamodel_fields = json_schema_to_dataclasses(
        json_schema=str_input_, with_import=with_import
    )
    if not res:  # pragma: no cover
        return None, None, None

    if isinstance(input_, Dict):
        # For some reason, the datamodel_code_generator logic turns "default": None into str 'None'
        res = res.replace("'None'", "None")

    return str_input_, res, datamodel_fields
