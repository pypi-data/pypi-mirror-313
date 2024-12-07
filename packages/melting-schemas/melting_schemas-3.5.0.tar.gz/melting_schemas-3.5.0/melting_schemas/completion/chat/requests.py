from pydantic import BaseModel, Field

from ..buffered_ml_messages import ChatMLMessage
from ..templating import TemplateInputs
from .settings import ChatModelSettings


class RawChatCompletionRequest(BaseModel):
    messages: list[ChatMLMessage]
    settings: ChatModelSettings


class ChatCompletionRequest(BaseModel):
    prompt_inputs: list[TemplateInputs]
    prompt_name: str
    settings: ChatModelSettings | None = None


class HybridChatCompletionRequest(BaseModel):
    prompt_name: str
    messages: list[ChatMLMessage | TemplateInputs]
    prompt_inputs: list[TemplateInputs] = Field(default_factory=list)
    settings: ChatModelSettings | None = None
