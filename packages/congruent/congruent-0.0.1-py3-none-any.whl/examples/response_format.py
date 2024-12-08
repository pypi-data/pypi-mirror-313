import os

import anthropic
import openai

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from congruent.llm.manager import pm
from congruent.llm.service import LLMService
from congruent.schemas.completion import CompletionRequest, Message

load_dotenv()


tagging_prompt = """
Extract the desired information from the following passage.

Only extract the properties mentioned in the 'Classification' function.

Passage:
{input}
"""


class Classification(BaseModel):
    sentiment: str = Field(description="The sentiment of the text")
    aggressiveness: int = Field(
        description="How aggressive the text is on a scale from 1 to 10"
    )
    language: str = Field(description="The language the text is written in")


def main():
    llm_openai = LLMService(client=openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"]))
    llm_anthropic = LLMService(
        client=anthropic.Client(api_key=os.environ["ANTHROPIC_API_KEY"])
    )

    content = tagging_prompt.format(
        input="Estoy increiblemente contento de haberte conocido! Creo que seremos muy buenos amigos!"
    )
    messages = [Message(role="user", content=content)]

    request = CompletionRequest(
        messages=messages,
        response_format=Classification,
        model="gpt-4o-2024-08-06",
        temperature=0.7,
        max_tokens=50,
    )

    response = llm_openai.get_completion(request)

    print("+-+" * 10)
    print(f"Response from {response.provider} ({response.model}): {response.parsed}")
    print("+-+" * 10)

    request = CompletionRequest(
        messages=messages,
        tools=[Classification],
        model="claude-3-5-sonnet-20241022",
        mode="json",
        temperature=0.7,
        max_tokens=50,
    )

    response = llm_anthropic.get_completion(request)
    print("+-+" * 10)
    print(
        f"Response from {response.provider} ({response.model}): {response.tool_calls}"
    )
    print("+-+" * 10)


if __name__ == "__main__":
    pm.register_default_providers()
    main()
