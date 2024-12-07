from typing import Annotated

from pydantic import BaseModel, Field


class BaseModelSettings(BaseModel):
    model: str
    max_tokens: int | None = Field(default=None, ge=1)  # defaults to inf
    temperature: float | None = Field(default=None, ge=0, le=2)
    top_p: float | None = Field(default=None, ge=0, le=1)
    logit_bias: dict[str, Annotated[int, Field(ge=-100, le=100)]] | None = None
    stop: list[str] | None = Field(default=None, max_length=4)
    presence_penalty: float = Field(default=0, ge=-2, le=2)
    frequency_penalty: float = Field(default=0, ge=-2, le=2)
