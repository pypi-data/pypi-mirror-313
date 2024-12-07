from pydantic import BaseModel

from ..usage import TokenUsage


class TextEncoding(BaseModel):
    model: str
    snippets: list[str]
    vectors: list[list[float]]

    usage: TokenUsage | None = None


class RawTextEncodingRequest(BaseModel):
    snippets: list[str]
    model: str
    dims: int | None = None
