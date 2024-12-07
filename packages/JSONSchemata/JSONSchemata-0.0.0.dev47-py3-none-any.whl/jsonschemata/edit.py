from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

if _TYPE_CHECKING:
    from typing import Callable


def required_last(schema: dict) -> dict:
    """Modify JSON schema to recursively put all 'required' fields at the end of the schema.

    This is done because otherwise the 'required' fields
    are checked by jsonschema before filling the defaults,
    which can cause the validation to fail.

    Returns
    -------
    dict
        Modified schema.
        Note that the input schema is modified in-place,
        so the return value is a reference to the (now modified) input schema.
    """
    if "required" in schema:
        schema["required"] = schema.pop("required")
    for key in ["anyOf", "allOf", "oneOf", "prefixItems"]:
        if key in schema:
            for subschema in schema[key]:
                required_last(subschema)
    for key in ["if", "then", "else", "not", "items", "unevaluatedItems", "contains", "additionalProperties", "patternProperties", "unevaluatedProperties"]:
        if key in schema and isinstance(schema[key], dict):
            required_last(schema[key])
    if "properties" in schema and isinstance(schema["properties"], dict):
        for subschema in schema["properties"].values():
            required_last(subschema)
    return schema


def add_property(
    schema: dict,
    prop: str,
    value: dict,
    conditioner: Callable[[dict, list], bool] | None = None,
    current_path: list[str] | None = None,
) -> dict:
    """Recursively add a property to a JSON schema.

    Parameters
    ----------
    schema : dict
        The JSON schema to modify.
    prop : str
        The name of the property to add.
    value : Any
        The value of the property to add.
    conditioner : Callable[[dict, list], bool], optional
        A function that takes a schema and the path to the current schema as arguments
        and returns a boolean indicating whether to add the property to the schema.
    current_path : list[str], optional
        The path to the current schema in the JSON schema hierarchy.
    Returns
    -------
    dict
        The modified schema.
    """
    if current_path is None:
        current_path = []
    for key in ["anyOf", "allOf", "oneOf", "prefixItems"]:
        if key in schema:
            for idx, subschema in enumerate(schema[key]):
                add_property(subschema, prop, value, conditioner, current_path + [f"{key}[{idx}]"])
    for key in ["if", "then", "else", "not", "items", "unevaluatedItems", "contains", "additionalProperties", "patternProperties", "unevaluatedProperties"]:
        if key in schema and isinstance(schema[key], dict):
            add_property(schema[key], prop, value, conditioner, current_path + [key])
    if "properties" in schema:
        for property_name, subschema in schema["properties"].items():
            add_property(subschema, prop, value, conditioner, current_path + [f"properties[{property_name}]"])
        if not conditioner or conditioner(schema, current_path):
            schema["properties"][prop] = value
    return schema
