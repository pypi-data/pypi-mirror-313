from typing import Annotated, Literal

from pydantic import BaseModel, Field


class ChatTextContent(BaseModel):
    type: Literal["text"] = "text"
    text: str


class ImageURL(BaseModel):
    url: str
    detail: Literal["low"] = "low"


class ChatImageContent(BaseModel):
    type: Literal["image_url"] = "image_url"
    image_url: ImageURL


class ChatMLMessage(BaseModel):
    content: str | list[ChatTextContent | ChatImageContent]
    name: Annotated[str, Field(pattern=r"^[a-zA-Z0-9_]*$", max_length=64)] | None = None
    role: Literal["user", "assistant", "system"]


class ToolCallFunction(BaseModel):
    arguments: str
    name: str


class ToolCall(BaseModel):
    id: str
    type: Literal["function"]
    function: ToolCallFunction


class ToolCallMLMessage(BaseModel):
    id: str
    content: None
    tool_calls: list[ToolCall]
    role: Literal["assistant"]


class ToolMLMessage(BaseModel):
    tool_id: str
    content: str
    name: str
    role: Literal["tool"]


BufferedMLMessageType = ChatMLMessage | ToolCallMLMessage | ToolMLMessage
