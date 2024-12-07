from pydantic import BaseModel


class RequestValidationError(BaseModel):
    loc: list[str]
    msg: str
    type: str


class HTTPErrorDetails(BaseModel):
    detail: RequestValidationError
