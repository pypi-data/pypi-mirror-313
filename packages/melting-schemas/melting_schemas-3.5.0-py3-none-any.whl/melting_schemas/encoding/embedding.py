from pydantic import BaseModel

from melting_schemas.usage import TokenUsage


class Embeddings(BaseModel):
    vectors: list[list[float]]
    model: str
    usage: TokenUsage | None = None
