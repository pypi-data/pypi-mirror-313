from melting_schemas.utils import wrap

from .requests import RawTextCompletionRequest
from .settings import TextModelSettings


def text_completion_examples():
    minimal = RawTextCompletionRequest(
        text="Hello World",
        settings=TextModelSettings(model="openai/gpt-3.5-turbo-instruct"),
    )
    with_suffix = RawTextCompletionRequest(
        text="# write a function that returns the sum of two numbers\n",
        settings=TextModelSettings(model="openai/gpt-3.5-turbo-instruct"),
        suffix="def sum(a, b):\n    return a + b\n",
    )

    return [wrap(name="Minimal", value=minimal), wrap(name="With Suffix", value=with_suffix)]
