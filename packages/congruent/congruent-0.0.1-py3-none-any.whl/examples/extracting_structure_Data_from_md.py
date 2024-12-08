import json
import os
import pandas as pd

from io import StringIO
from textwrap import dedent
from typing import Annotated, Any, Iterable

import anthropic
import openai

from dotenv import load_dotenv
from pydantic import (
    BaseModel,
    BeforeValidator,
    InstanceOf,
    PlainSerializer,
    WithJsonSchema,
)

from congruent.llm.manager import pm
from congruent.llm.service import LLMService
from congruent.schemas.completion import CompletionRequest, Message

load_dotenv()


def md_to_df(data: Any) -> Any:
    # Convert markdown to DataFrame
    if isinstance(data, str):
        return (
            pd.read_csv(
                StringIO(data),  # Process data
                sep="|",
                index_col=1,
            )
            .dropna(axis=1, how="all")
            .iloc[1:]
            .applymap(lambda x: x.strip())
        )
    return data


MarkdownDataFrame = Annotated[
    InstanceOf[pd.DataFrame],
    BeforeValidator(md_to_df),
    PlainSerializer(lambda df: df.to_markdown()),
    WithJsonSchema(
        {
            "type": "string",
            "description": "The markdown representation of the table, each one should be tidy, do not try to join tables that should be seperate",
        }
    ),
]


class Table(BaseModel):
    caption: str
    dataframe: MarkdownDataFrame


def main():
    llm_openai = LLMService(client=openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"]))
    llm_anthropic = LLMService(
        client=anthropic.Client(api_key=os.environ["ANTHROPIC_API_KEY"])
    )

    url = "https://a.storyblok.com/f/47007/2400x2000/bf383abc3c/231031_uk-ireland-in-three-charts_table_v01_b.png"

    system_message = dedent(
        f"""
        As a genius expert, your task is to understand the content and provide
        the parsed objects in json that match the following json_schema:\n

        {json.dumps(Table.model_json_schema(), indent=2, ensure_ascii=False)}

        Make sure to return an instance of the JSON, not the schema itself
        """
    )
    messages = [
        Message(
            role="system",
            content=system_message,
        ),
        Message(
            role="user",
            content=[
                {"type": "text", "text": "Extract table from image."},
                {"type": "image_url", "image_url": {"url": url}},
                {
                    "type": "text",
                    "text": "Return the correct JSON response within a ```json codeblock. not the JSON_SCHEMA",
                },
            ],
        ),
    ]

    # OpenAI
    request = CompletionRequest(
        messages=messages,
        model="gpt-4o-mini",
        mode="json",
        max_tokens=1800,
    )
    response = llm_openai.get_completion(request)

    data = json.loads(response.content)
    for table in data:
        print(table)
        print(data[table])

    # Anthropic
    request = CompletionRequest(
        messages=messages,
        model="claude-3-5-sonnet-20240620",
        mode="json",
        max_tokens=1800,
    )
    response = llm_anthropic.get_completion(request)
    data = json.loads(response.content)
    for table in data:
        print(table)
        print(data[table])


if __name__ == "__main__":
    pm.register_default_providers()
    main()
