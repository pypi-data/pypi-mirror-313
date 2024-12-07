from typing import Protocol

from fastapi.openapi.models import Example
from pydantic import BaseModel


class NamedDumpable(Protocol):
    name: str

    model_dump = BaseModel.model_dump


class OpenAPIExample(BaseModel):
    name: str
    value: BaseModel


def wrap(name: str, value: BaseModel) -> NamedDumpable:
    return OpenAPIExample(name=name, value=value)


def to_openapi_examples(examples: list[NamedDumpable | OpenAPIExample]) -> dict[str, Example]:
    """
    Convert a list of objects to a dictionary of OpenAPI Examples.

    It accepts a list of NamedDumpable compatible objects or OpenAPIExample objects.

    NamedDumpable objects are expected to have a `name` attribute and a `model_dump` method
    with the same signature as pydantic's `BaseModel.model_dump` method.

    Usage example:
    ```python
        from pydantic import BaseModel

        from melting_schemas.utils import to_openapi_examples, wrap


        class NamedModel(BaseModel):
            name: str
            age: int


        # Named models can be used as is
        examples = to_openapi_examples([NamedModel(name="John", age=30)])
        print(examples)


        class UnnamedModel(BaseModel):
            age: int


        # Unnamed models need to be wrapped to be used
        example = wrap(name="John", value=UnnamedModel(age=30))
        examples = to_openapi_examples([example])
        print(examples)
    ```

    Args:
        examples: A list of NamedDumpable compatible objects or OpenAPIExample objects.

    Returns:
        A dictionary of OpenAPI Examples
    """

    openapi_examples = {}
    for example in examples:
        if isinstance(example, OpenAPIExample):
            value = example.value.model_dump(by_alias=True, exclude_unset=True)
        else:
            value = example.model_dump(by_alias=True, exclude_unset=True)
        openapi_examples[example.name] = Example(value=value)
    return openapi_examples
