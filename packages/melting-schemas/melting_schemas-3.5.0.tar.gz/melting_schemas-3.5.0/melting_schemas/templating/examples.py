from prompts.turbo import PromptRole, TemplateInputs

from melting_schemas.utils import wrap

from ..completion.chat import ChatModelSettings
from .prompt import ChatPromptTemplate, Template


def chat_prompt_template_examples():
    minimal_prompt_template = ChatPromptTemplate(
        assistant_templates="<text>",
        description="Single of its kind, example app, teia org.",
        name="teia.example_app.single.example01",
        system_templates="<text>",
        user_templates="<text>",
        initial_template_data=[
            TemplateInputs(role=PromptRole.SYSTEM, name="", inputs={"a": "a"}, template_name="name")
        ],
        settings=ChatModelSettings(model="gpt-3.5-turbo"),
    )

    timeaware_prompt_template = ChatPromptTemplate(
        assistant_templates="<text>",
        description="Single of its kind, example app, teia org.",
        name="teia.example.1",
        system_templates="Current timestamp: <now>\nYou are a helpful chatbot.",
        user_templates="<text>",
        settings=ChatModelSettings(model="gpt-3.5-turbo"),
    )

    many_template = ChatPromptTemplate(
        name="teia.example.2",
        description="A development example.",
        system_templates=[
            Template(template_name="plugin_prompt", template="<plugin_data>"),
        ],
        user_templates=[
            Template(template_name="user_prompt", template="<question>"),
        ],
        assistant_templates=[
            Template(template_name="assistant_prompt", template="<message>"),
        ],
        settings=ChatModelSettings(
            model="gpt-3.5-turbo",
            max_tokens=200,
            temperature=0.25,
        ),
    )

    return [
        wrap(name="Minimal prompt template", value=minimal_prompt_template),
        wrap(name="Time-aware prompt template", value=timeaware_prompt_template),
        wrap(name="Many template", value=many_template),
    ]
