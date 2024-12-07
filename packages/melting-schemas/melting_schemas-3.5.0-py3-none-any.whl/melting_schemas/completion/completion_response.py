from typing import Literal

from pydantic import BaseModel, Field

from melting_schemas.completion.base_settings import BaseModelSettings
from melting_schemas.completion.buffered_ml_messages import (
    BufferedMLMessageType,
    ChatMLMessage,
    ToolCallMLMessage,
)
from melting_schemas.completion.finish_reason import FinishReason
from melting_schemas.completion.tcall import ToolInfo
from melting_schemas.completion.templating import Templating
from melting_schemas.usage import StreamTimings, Timings, TokenUsage


class CompletionResponse[T: (StreamTimings, Timings), S: BaseModelSettings](BaseModel):
    # Context
    messages: list[BufferedMLMessageType] = Field(default_factory=list)
    tools: list[ToolInfo] = Field(default_factory=list)
    templating: Templating | None = None

    # Out
    output: ChatMLMessage | ToolCallMLMessage | str

    # Analytics
    finish_reason: FinishReason
    timings: T
    usage: TokenUsage

    # Config
    type: Literal["chat", "tcall", "text"]
    settings: S
