import inspect

from typing import Any, Callable, Optional, Union

from clipped.compact.pydantic import Field, create_model
from docstring_parser import parse


def _recursive_set_additional_properties_false(
    schema: dict[str, Any],
) -> dict[str, Any]:
    """Recursively set additionalProperties to False in a JSON Schema.

    This function ensures that the 'additionalProperties' key is set to False in a JSON Schema
    to prevent the addition of new properties. It recursively checks nested properties.

    Args:
        schema: A dictionary representing a JSON Schema.

    Returns:
        dict: The modified JSON Schema with 'additionalProperties' set to False.
    """
    if isinstance(schema, dict):
        # Check if 'required' is a key at the current level or if the schema is empty,
        # in which case additionalProperties still needs to be specified.
        if "required" in schema or (
            "properties" in schema and not schema["properties"]
        ):
            schema["additionalProperties"] = False

        # Recursively check 'properties' and 'items' if they exist
        if "properties" in schema:
            for value in schema["properties"].values():
                _recursive_set_additional_properties_false(value)
        if "items" in schema:
            _recursive_set_additional_properties_false(schema["items"])

    return schema


def convert_to_openai_function(
    obj: Union[dict[str, Any], type, Callable],
    *,
    strict: Optional[bool] = None,
) -> dict[str, Any]:
    """Convert a raw function/class/dict to an OpenAI function schema.

    This function handles multiple input formats and converts them to the OpenAI function schema format
    used for function calling. The following input formats are supported:

    - Dictionary in OpenAI function format (with name, description, parameters)
    - Dictionary in JSON Schema format (with title, description, properties)
    - Dictionary in Anthropic tool format (with name, description, input_schema)
    - Dictionary in Amazon Bedrock Converse format (with toolSpec)
    - Pydantic BaseModel class
    - Python function/callable

    Args:
        obj: The object to convert. Can be a dictionary in one of the supported formats,
            a Pydantic BaseModel class, or a Python callable.
        strict: If True, enforces strict JSON Schema validation on model output.
            If None, the strict validation flag is omitted from the schema.

    Returns:
        dict: A dictionary in OpenAI function schema format containing:
            - name: The function name
            - description: The function description
            - parameters: The JSON Schema for the function parameters

    Raises:
        ValueError: If the input object format is not supported or cannot be converted.
    """

    obj_schema = None
    # already in OpenAI function format
    if isinstance(obj, dict) and all(
        k in obj for k in ("name", "description", "parameters")
    ):
        obj_schema = obj
    # a JSON schema with title and description
    if (
        not obj_schema
        and isinstance(obj, dict)
        and all(k in obj for k in ("title", "description", "properties"))
    ):
        obj = obj.copy()
        obj_schema = {
            "name": obj.pop("title"),
            "description": obj.pop("description"),
            "parameters": obj,
        }
    # an Anthropic format tool
    if (
        not obj_schema
        and isinstance(obj, dict)
        and all(k in obj for k in ("name", "description", "input_schema"))
    ):
        obj_schema = {
            "name": obj["name"],
            "description": obj["description"],
            "parameters": obj["input_schema"],
        }
    # an Amazon Bedrock Converse format tool
    if not obj_schema and isinstance(obj, dict) and "toolSpec" in obj:
        obj_schema = {
            "name": obj["toolSpec"]["name"],
            "description": obj["toolSpec"]["description"],
            "parameters": obj["toolSpec"]["inputSchema"]["json"],
        }
    # a Pydantic BaseModel
    if not obj_schema and isinstance(obj, type):
        obj_schema = convert_pydantic_to_schema(obj)
    if not obj_schema and callable(obj):
        # Create a schema from the function signature
        function_model = function_to_pydantic_model(obj)
        obj_schema = convert_pydantic_to_schema(function_model)
    if not obj_schema:
        msg = (
            f"Unsupported function\n\n{obj}\n\nFunctions must be passed in"
            " as Dict, pydantic.BaseModel, or Callable. If they're a dict they must"
            " either be in OpenAI function format or valid JSON schema with top-level"
            " 'title' and 'description' keys."
        )
        raise ValueError(msg)

    if strict is not None:
        obj_schema["strict"] = strict
        if strict:
            # As of 08/06/24, OpenAI requires that additionalProperties be supplied and
            # set to False if strict is True.
            # All properties layer needs 'additionalProperties=False'
            obj_schema["parameters"] = _recursive_set_additional_properties_false(
                obj_schema["parameters"]
            )
    return obj_schema


def convert_pydantic_to_schema(
    pydantic_model: type,
) -> dict[str, Any]:
    """Convert a Pydantic BaseModel to a JSON Schema.

    This function extracts the JSON Schema from a Pydantic BaseModel using the appropriate method
    based on the Pydantic version.

    Args:
        pydantic_model: The Pydantic BaseModel to convert.

    Returns:
        dict: A dictionary representing the JSON Schema.
    """
    if hasattr(pydantic_model, "model_json_schema"):
        schema = pydantic_model.model_json_schema()  # Pydantic 2
    elif hasattr(pydantic_model, "schema"):
        schema = pydantic_model.schema()  # Pydantic 1
    else:
        return {}

    # Inline any nested models from $defs
    if "$defs" in schema:

        def resolve_refs(obj):
            if isinstance(obj, dict):
                if "$ref" in obj and obj["$ref"].startswith("#/$defs/"):
                    ref_name = obj["$ref"].split("/")[-1]
                    resolved = schema["$defs"][ref_name].copy()
                    # Preserve any existing keys from the ref object (like description)
                    resolved.update({k: v for k, v in obj.items() if k != "$ref"})
                    return resolved
                return {k: resolve_refs(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [resolve_refs(item) for item in obj]
            return obj

        schema = resolve_refs(schema)

    docstring = parse(pydantic_model.__doc__ or "")
    parameters = {k: v for k, v in schema.items() if k not in ("title", "description")}
    for param in docstring.params:
        if (param_name := param.arg_name) in parameters["properties"] and (
            param_description := param.description
        ):
            if "description" not in parameters["properties"][param_name]:
                parameters["properties"][param_name]["description"] = param_description

    parameters["required"] = sorted(
        k for k, v in parameters["properties"].items() if "default" not in v
    )

    return {
        "name": schema.get("title", pydantic_model.__name__),
        "description": schema.get("description", docstring.short_description or ""),
        "parameters": parameters,
    }


def function_to_pydantic_model(func):
    """Convert a Python function to a Pydantic BaseModel.

    This function extracts the parameters from a Python function's signature and creates a Pydantic BaseModel
    with fields corresponding to the function's parameters.

    Args:
        func: The Python function to convert.

    Returns:
        Pydantic BaseModel: A Pydantic BaseModel with fields corresponding to the function's parameters.
    """
    # Parse the function signature
    signature = inspect.signature(func)

    # Extract docstring info
    docstring_params = {}
    if func.__doc__:
        doc = parse(func.__doc__)
        docstring_params = {param.arg_name: param.description for param in doc.params}

    # Create field definitions
    fields = {}
    for name, param in signature.parameters.items():
        field_type = param.annotation
        description = docstring_params.get(name, f"Parameter: {name}")

        # Handle Optional types
        default = ... if param.default == param.empty else param.default
        if hasattr(field_type, "__origin__") and field_type.__origin__ is Union:
            # Check if it's Optional (Union with NoneType)
            types = field_type.__args__
            if type(None) in types:
                # Get the actual type (excluding NoneType)
                field_type = next(t for t in types if t != type(None))
                default = None if param.default == param.empty else param.default

        fields[name] = (field_type, Field(default=default, description=description))

    # Create dynamic model
    model_name = f"{func.__name__.title()}Model"
    return create_model(model_name, **fields)
