from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    """
    Generic keywords shared amongst schemas based on JSON Schema spec:
    https://json-schema.org/understanding-json-schema/reference/generic
    """

    enum: list[str | None | int | float | bool] = Field(default_factory=list)

    # Docs
    comment: str = Field(default="", alias="$comment")
    description: str = ""
    title: str = ""

    # Examples
    default: Any = None
    examples: list[Any] = Field(default_factory=list)

    # Flags
    deprecated: bool = False
    read_only: bool = Field(default=False, alias="readOnly")
    write_only: bool = Field(default=False, alias="writeOnly")

    model_config = ConfigDict(populate_by_name=True)


class StringSchema(BaseSchema):
    """
    String schema following JSON Schema spec:
    https://json-schema.org/understanding-json-schema/reference/numeric
    """

    type: Literal["string"]

    # Built-in formats: https://json-schema.org/understanding-json-schema/reference/string#built-in-formats
    format: str = ""

    # Validation
    pattern: str = ""
    max_length: int = Field(default=0, alias="maxLength")
    min_length: int = Field(default=0, alias="minLength")


class NumberSchema(BaseSchema):
    """
    Boolean schema following JSON Schema spec:
    https://json-schema.org/understanding-json-schema/reference/numeric
    """

    type: Literal["integer", "number"]
    multiple_of: int = Field(default=0, alias="multipleOf")
    minimum: int = Field(default=0, alias="minimum")
    maximum: int = Field(default=0, alias="maximum")

    exclusive_minimum: int = Field(default=0, alias="exclusiveMinimum")
    exclusive_maximum: int = Field(default=0, alias="exclusiveMaximum")


class BooleanSchema(BaseSchema):
    """
    Boolean schema following JSON Schema spec:
    https://json-schema.org/understanding-json-schema/reference/boolean
    """

    type: Literal["boolean"]


class NullSchema(BaseSchema):
    """
    Null schema following JSON Schema spec:
    https://json-schema.org/understanding-json-schema/reference/null
    """

    type: Literal["null"]


class ArraySchema(BaseSchema):
    """
    Array schema following JSON Schema spec:
    https://json-schema.org/understanding-json-schema/reference/array
    """

    type: Literal["array"]
    items: "Schemas | None" = Field(default=None)
    prefix_items: list["Schemas"] = Field(default_factory=list, alias="prefixItems")
    additional_items: "Schemas | None" = Field(default=None, alias="additionalItems")
    max_items: int = Field(default=0, alias="maxItems")
    min_items: int = Field(default=0, alias="minItems")
    unique_items: bool = Field(default=False, alias="uniqueItems")
    contains: "Schemas | None" = Field(default=None)
    min_contains: int = Field(default=0, alias="minContains")
    max_contains: int = Field(default=0, alias="maxContains")


class ObjectSchema(BaseSchema):
    """
    Object schema following JSON Schema spec:
    https://json-schema.org/understanding-json-schema/reference/object
    """

    type: Literal["object"]
    max_properties: int = Field(default=0, alias="maxProperties")
    min_properties: int = Field(default=0, alias="minProperties")
    properties: dict[str, "Schemas"] = Field(default_factory=dict)
    required: list[str] = Field(default_factory=list)


PrimitiveSchemas = StringSchema | NumberSchema | BooleanSchema | NullSchema
Schemas = ArraySchema | ObjectSchema | PrimitiveSchemas


class FunctionJsonSchema(BaseModel):
    name: str
    description: str = ""
    parameters: ObjectSchema | None = None


class FunctionJsonSchemaOverrides(BaseModel):
    name: str | None = None
    description: str | None = None
    parameters: ObjectSchema | None = None


BaseSchema.model_rebuild()
ArraySchema.model_rebuild()
ObjectSchema.model_rebuild()
