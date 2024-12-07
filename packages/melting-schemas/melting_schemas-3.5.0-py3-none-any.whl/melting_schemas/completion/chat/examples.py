from datetime import datetime

from melting_schemas.utils import wrap

from ..buffered_ml_messages import (
    ChatImageContent,
    ChatMLMessage,
    ChatTextContent,
    ImageURL,
)
from ..templating import TemplateInputs
from .requests import (
    ChatCompletionRequest,
    HybridChatCompletionRequest,
    RawChatCompletionRequest,
)
from .settings import ChatModelSettings


def raw_chat_completion_request_examples():
    raw = RawChatCompletionRequest(
        messages=[
            ChatMLMessage(content="You are a helpful chatbot.", role="system"),
            ChatMLMessage(content="What does bequeath mean?", role="user"),
        ],
        settings=ChatModelSettings(model="openai/gpt-3.5-turbo-1106"),
    )
    named_raw = RawChatCompletionRequest(
        messages=[
            ChatMLMessage(content="You are a helpful chatbot.", role="system"),
            ChatMLMessage(content="What does my name mean?", name="John", role="user"),
        ],
        settings=ChatModelSettings(model="openai/gpt-4-0613"),
    )
    multimodal_raw = RawChatCompletionRequest(
        messages=[
            ChatMLMessage(content="You are a helpful chatbot.", role="system"),
            ChatMLMessage(
                content=[
                    ChatTextContent(text="What's Severo's favorite food? (tip: image)"),
                    ChatImageContent(
                        image_url=ImageURL(
                            url="https://upload.wikimedia.org/wikipedia/commons/a/ab/Patates.jpg",
                            detail="low",
                        ),
                    ),
                ],
                role="user",
            ),
        ],
        settings=ChatModelSettings(model="openai/gpt-4o"),
    )

    return [
        wrap(name="Raw", value=raw),
        wrap(name="Named Raw", value=named_raw),
        wrap(name="Multimodal Raw", value=multimodal_raw),
    ]


def chat_completion_request_examples():
    prompted = ChatCompletionRequest(
        prompt_inputs=[
            TemplateInputs(role="system", inputs={"now": str(datetime.now())}),
            TemplateInputs(role="user", inputs={"text": "What day is today?"}),
        ],
        prompt_name="teia.example.1",
    )
    many_templates = ChatCompletionRequest(
        prompt_inputs=[
            TemplateInputs(
                role="system",
                inputs={"plugin_data": "Secret number is 42"},
                template_name="plugin_prompt",
            ),
            TemplateInputs(
                role="user",
                inputs={"question": "What is the secret number???"},
                template_name="user_prompt",
            ),
        ],
        prompt_name="teia.example.2",
    )
    return [
        wrap(name="Prompted", value=prompted),
        wrap(name="Many Templates", value=many_templates),
    ]


def hybrid_request_examples():
    hybrid = HybridChatCompletionRequest(
        messages=[
            ChatMLMessage(content="You are a helpful chatbot.", role="system"),
            TemplateInputs(role="user", inputs={"text": "What day is today?"}),
        ],
        prompt_name="teia.example.1",
    )
    return [wrap(name="Hybrid", value=hybrid)]
