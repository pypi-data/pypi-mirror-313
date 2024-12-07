from typing import Any

from pydantic import BaseModel, Field


class StaticParams(BaseModel):
    query: dict[str, Any] = Field(default_factory=dict)
    body: dict[str, Any] = Field(default_factory=dict)


class GeneratedParams(BaseModel):
    path: list[str] = Field(default_factory=list)
    query: list[str] = Field(default_factory=list)
    body: list[str] = Field(default_factory=list)


class Forwardings(BaseModel):
    headers: list[str] = Field(default_factory=list)
    path: list[str] = Field(default_factory=list)
    query: list[str] = Field(default_factory=list)
    body: list[str] = Field(default_factory=list)


class StaticTool(BaseModel):
    name: str
    arguments: dict[str, Any]
    response: Any | None = None
