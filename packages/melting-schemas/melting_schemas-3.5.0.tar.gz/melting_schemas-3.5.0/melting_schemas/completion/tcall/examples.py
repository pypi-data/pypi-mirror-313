from melting_schemas.json_schema import FunctionJsonSchema, ObjectSchema, StringSchema
from melting_schemas.utils import wrap

from ..buffered_ml_messages import ChatMLMessage
from ..templating import TemplateInputs
from .params import Forwardings, StaticTool
from .requests import PromptedTCallRequest, RawTCallRequest
from .settings import TCallModelSettings
from .specs import (
    GeneratedParams,
    HttpToolCallee,
    StaticParams,
    ToolJsonSchema,
    ToolSpec,
)


def raw_tcall_request_examples():
    json_schema_tcall = RawTCallRequest(
        tools=[
            ToolJsonSchema(
                type="function",
                function=FunctionJsonSchema(
                    name="weather",
                    description="Retrieve weather information based on a city's name.",
                    parameters=ObjectSchema(
                        type="object",
                        properties={
                            "city_name": StringSchema(
                                type="string",
                                description="Name of the city.",
                            )
                        },
                        required=["city_name"],
                    ),
                ),
            )
        ],
        messages=[ChatMLMessage(content="How is the weather in Paris?", role="user")],
        settings=TCallModelSettings(model="gpt-4o"),
    )

    tool_spec_tcall = RawTCallRequest(
        tools=[
            ToolSpec(
                tool_name="weather_tool",
                callee=HttpToolCallee(
                    method="GET",
                    forwardings=Forwardings(headers=["authorization"]),
                    url="https://plugins.beta.allai.digital/weather-plugin/weather_current",
                    static_params=StaticParams(query={"kwargs": ""}),
                    generated_params=GeneratedParams(query=["place"]),
                    parameter_translator={"city_name": "place"},
                ),
                json_schema=ToolJsonSchema(
                    type="function",
                    function=FunctionJsonSchema(
                        name="weather",
                        description="Retrieve weather information based on a city's name.",
                        parameters=ObjectSchema(
                            type="object",
                            properties={
                                "city_name": StringSchema(
                                    type="string",
                                    description="Name of the city.",
                                )
                            },
                            required=["city_name"],
                        ),
                    ),
                ),
            )
        ],
        messages=[ChatMLMessage(content="How is the weather in Paris?", role="user")],
        settings=TCallModelSettings(model="gpt-4o"),
    )

    native_tcall = RawTCallRequest(
        tools=["weather_plugin"],
        messages=[ChatMLMessage(content="How is the weather in Paris?", role="user")],
        settings=TCallModelSettings(model="gpt-4o"),
    )

    return [
        wrap(name="Raw Json Schema Request", value=json_schema_tcall),
        wrap(name="Tool Calling Request", value=tool_spec_tcall),
        wrap(name="Native Tool Calling Request", value=native_tcall),
    ]


def prompted_tcall_request_examples():
    json_schema_tcall = PromptedTCallRequest(
        tools=[
            ToolJsonSchema(
                type="function",
                function=FunctionJsonSchema(
                    name="weather",
                    description="Retrieve weather information based on a city's name.",
                    parameters=ObjectSchema(
                        type="object",
                        properties={
                            "city_name": StringSchema(
                                type="string",
                                description="Name of the city.",
                            )
                        },
                        required=["city_name"],
                    ),
                ),
            )
        ],
        prompt_name="weather_prompt",
        prompt_inputs=[TemplateInputs(inputs={"city_name": "Paris"}, role="user")],
        settings=TCallModelSettings(model="gpt-4o"),
    )

    tool_spec_tcall = PromptedTCallRequest(
        tools=[
            ToolSpec(
                tool_name="weather_tool",
                callee=HttpToolCallee(
                    method="GET",
                    forwardings=Forwardings(headers=["authorization"]),
                    url="https://plugins.beta.allai.digital/weather-plugin/weather_current",
                    static_params=StaticParams(query={"kwargs": ""}),
                    generated_params=GeneratedParams(query=["place"]),
                    parameter_translator={"city_name": "place"},
                ),
                json_schema=ToolJsonSchema(
                    type="function",
                    function=FunctionJsonSchema(
                        name="weather",
                        description="Retrieve weather information based on a city's name.",
                        parameters=ObjectSchema(
                            type="object",
                            properties={
                                "city_name": StringSchema(
                                    type="string",
                                    description="Name of the city.",
                                )
                            },
                            required=["city_name"],
                        ),
                    ),
                ),
            )
        ],
        prompt_name="weather_prompt",
        prompt_inputs=[TemplateInputs(inputs={"city_name": "Paris"}, role="user")],
        settings=TCallModelSettings(model="gpt-4o"),
    )

    native_tcall = PromptedTCallRequest(
        tools=["weather_plugin"],
        prompt_name="weather_prompt",
        prompt_inputs=[TemplateInputs(inputs={"city_name": "Paris"}, role="user")],
        settings=TCallModelSettings(model="gpt-4o"),
    )

    return [
        wrap(name="Raw Prompted Json Schema Request", value=json_schema_tcall),
        wrap(name="Tool Calling Prompted Request", value=tool_spec_tcall),
        wrap(name="Native Tool Calling Prompted Request", value=native_tcall),
    ]


def special_tcall_request_examples():
    json_schema_tcall = RawTCallRequest(
        tools=[
            ToolJsonSchema(
                type="function",
                function=FunctionJsonSchema(
                    name="weather",
                    description="Retrieve weather information based on a city's name.",
                    parameters=ObjectSchema(
                        type="object",
                        properties={
                            "city_name": StringSchema(
                                type="string",
                                description="Name of the city.",
                            )
                        },
                        required=["city_name"],
                    ),
                ),
            )
        ],
        static_tools=[StaticTool(name="locator", arguments={}, response="User lives in Paris")],
        messages=[ChatMLMessage(content="How is the weather in Paris?", role="user")],
        settings=TCallModelSettings(model="gpt-4o"),
    )

    tool_spec_tcall = RawTCallRequest(
        tools=[
            ToolSpec(
                tool_name="weather_tool",
                callee=HttpToolCallee(
                    method="GET",
                    forwardings=Forwardings(headers=["authorization"]),
                    url="https://plugins.beta.allai.digital/weather-plugin/weather_current",
                    static_params=StaticParams(query={"kwargs": ""}),
                    generated_params=GeneratedParams(query=["place"]),
                    parameter_translator={"city_name": "place"},
                ),
                json_schema=ToolJsonSchema(
                    type="function",
                    function=FunctionJsonSchema(
                        name="weather",
                        description="Retrieve weather information based on a city's name.",
                        parameters=ObjectSchema(
                            type="object",
                            properties={
                                "city_name": StringSchema(
                                    type="string",
                                    description="Name of the city.",
                                )
                            },
                            required=["city_name"],
                        ),
                    ),
                ),
            )
        ],
        static_tools=[StaticTool(name="locator", arguments={}, response="User lives in Paris")],
        messages=[ChatMLMessage(content="How is the weather in Paris?", role="user")],
        settings=TCallModelSettings(model="gpt-4o"),
    )

    native_tcall = RawTCallRequest(
        tools=["weather_plugin"],
        static_tools=[StaticTool(name="locator", arguments={}, response="User lives in Paris")],
        messages=[ChatMLMessage(content="How is the weather in Paris?", role="user")],
        settings=TCallModelSettings(model="gpt-4o"),
    )

    return [
        wrap(name="Raw Json Schema Request", value=json_schema_tcall),
        wrap(name="Tool Calling Request", value=tool_spec_tcall),
        wrap(name="Native Tool Calling Request", value=native_tcall),
    ]
