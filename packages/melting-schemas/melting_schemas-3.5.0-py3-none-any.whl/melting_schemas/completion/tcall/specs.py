from typing import Any, Literal

from pydantic import BaseModel, Field, SerializeAsAny

from melting_schemas.json_schema import FunctionJsonSchema, FunctionJsonSchemaOverrides

from .params import Forwardings, GeneratedParams, StaticParams


class NoopToolCallee(BaseModel):
    type: Literal["noop"] = "noop"


class HttpToolCallee(BaseModel):
    type: Literal["http"] = "http"
    method: Literal["GET", "POST"]
    headers: dict[str, str] = Field(default_factory=dict)
    url: str
    forwardings: Forwardings = Field(default_factory=Forwardings)
    static_params: StaticParams = Field(default_factory=StaticParams)
    generated_params: GeneratedParams = Field(default_factory=GeneratedParams)
    parameter_translator: dict[str, str] = Field(default_factory=dict)


class ToolJsonSchema(BaseModel):
    type: Literal["function"] = "function"
    function: FunctionJsonSchema


class ToolSpec(BaseModel):
    tool_name: str
    callee: HttpToolCallee | NoopToolCallee
    json_schema: ToolJsonSchema


class UpdateToolSpec(BaseModel):
    tool_name: str | None = None
    callee: HttpToolCallee | NoopToolCallee | None = None
    json_schema: ToolJsonSchema | None = None


class ToolInfo(BaseModel):
    spec: SerializeAsAny[ToolSpec | FunctionJsonSchema]
    ml_message_id: Any = None


class CallableStaticTool(BaseModel):
    name: str
    arguments: dict[str, Any]
    callee: HttpToolCallee | NoopToolCallee
    ml_message_id: Any = None


class HttpToolCalleeOverrides(BaseModel):
    static_params: StaticParams = Field(default_factory=StaticParams)


class ToolSpecOverride(BaseModel):
    function_override: FunctionJsonSchemaOverrides | None = None
    callee_override: HttpToolCalleeOverrides | None = None
