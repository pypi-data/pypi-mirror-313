from melting_schemas.completion.tcall.params import (
    Forwardings,
    GeneratedParams,
    StaticParams,
)
from melting_schemas.completion.tcall.specs import (
    HttpToolCallee,
    ToolJsonSchema,
    ToolSpec,
)
from melting_schemas.json_schema import (
    ArraySchema,
    FunctionJsonSchema,
    ObjectSchema,
    StringSchema,
)
from melting_schemas.utils import wrap


def create_tool_examples():
    tool_with_static_call = ToolSpec(
        callee=HttpToolCallee(
            type="http",
            method="POST",
            forwardings=Forwardings(headers=[]),
            headers={"authorization": "Bearer <melt-token>"},
            url="https://search.allai.digital/search/",
            static_params=StaticParams(query={}, body={}),
            generated_params=GeneratedParams(path=[], query=[], body=["query", "search_settings"]),
        ),
        json_schema=ToolJsonSchema(
            type="function",
            function=FunctionJsonSchema(
                name="rag-search-salesforce-help",
                description="Perform a semantic search on Salesforce Help documentation pages (https://help.salesforce.com/).",
                parameters=ObjectSchema(
                    type="object",
                    properties={
                        "query": StringSchema(
                            type="string",
                            description="The search query to be embedded.",
                        ),
                        "search_settings": ArraySchema(
                            type="array",
                            items=ObjectSchema(
                                type="object",
                                properties={
                                    "kb_name": StringSchema(
                                        type="string",
                                        description="Enum: ['salesforce_help_may_2024'].",
                                    )
                                },
                                required=["kb_name"],
                            ),
                        ),
                    },
                    required=["query", "search_settings"],
                ),
            ),
        ),
        tool_name="temp-help-salesforce-search",
    )

    return [wrap(name="Basic Tool Call", value=tool_with_static_call)]
