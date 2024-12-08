import os

from typing import Literal

import anthropic
import openai

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from congruent.llm.manager import pm
from congruent.llm.service import LLMService
from congruent.schemas.completion import CompletionRequest, Message

load_dotenv()

pm.register_default_providers()
llm_openai = LLMService(client=openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"]))
llm_anthropic = LLMService(
    client=anthropic.Client(api_key=os.environ["ANTHROPIC_API_KEY"])
)


class Search(BaseModel):
    query: str = Field(..., description="Query to search for relevant content")
    type: Literal["web", "image", "video"] = Field(..., description="Type of search")

    async def execute(self):
        print(
            f"Searching for `{self.title}` with query `{self.query}` using `{self.type}`"
        )


class SearchPlan(BaseModel):
    searches: list[Search]


def segment(data: str) -> SearchPlan:
    messages = [
        Message(
            role="user",
            content=f"Consider the data below: '\n{data}' and segment it into multiple search queries",
        ),
    ]
    request = CompletionRequest(
        model="gpt-4o-mini",
        response_format=SearchPlan,
        mode="json",
        messages=messages,
        max_tokens=1000,
    )
    result = llm_openai.get_completion(request)
    return result.parsed.searches


for search in segment("Search for a picture of a cat and a video of a dog"):
    print(search.model_dump_json())
    # > {"query":"picture of a cat","type":"image"}
    # > {"query":"video of a dog","type":"video"}
