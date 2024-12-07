from typing import Any, Literal

from pydantic import BaseModel


class ChatMLMessageChunk(BaseModel):
    type: Literal["chat"]
    id: Any
    delta: str


class ToolCallFunctionChunk(BaseModel):
    delta: str
    name: str | None = None


class ToolCallChunk(BaseModel):
    type: Literal["function"]
    id: Any
    tool_id: str
    function: ToolCallFunctionChunk


class ToolMLMessageChunk(BaseModel):
    type: Literal["tool_response"]
    tool_id: str
    delta: str
    name: str
    role: Literal["tool"]
