from pydantic import BaseModel

from .settings import TextModelSettings


class RawTextCompletionRequest(BaseModel):
    text: str
    settings: TextModelSettings
    suffix: str | None = None
