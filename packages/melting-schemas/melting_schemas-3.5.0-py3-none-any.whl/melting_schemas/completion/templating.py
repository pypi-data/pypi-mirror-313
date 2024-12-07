from typing import Literal

from pydantic import BaseModel


class TemplateInputs(BaseModel):
    inputs: dict[str, str]
    name: str | None = None
    role: Literal["user", "system", "assistant"]
    template_name: str | None = None  # Advanced usage: select sub-templates


class Templating(BaseModel):
    prompt_inputs: list[TemplateInputs | dict]
    prompt_id: str
    prompt_name: str
