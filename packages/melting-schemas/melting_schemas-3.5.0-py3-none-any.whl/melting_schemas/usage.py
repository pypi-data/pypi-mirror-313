from pydantic import BaseModel

from .completion.finish_reason import FinishReason


class TokenUsage(BaseModel):
    prompt_tokens: int
    total_tokens: int
    completion_tokens: int | None = None


class Timings(BaseModel):
    total: float


class StreamTimings(BaseModel):
    avg: float
    first: float
    max: float
    min: float
    total: float


class StreamUsageInfo(BaseModel):
    finish_reason: FinishReason
    token_usage: TokenUsage
    timings: StreamTimings
