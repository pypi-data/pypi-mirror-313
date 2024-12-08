import os

import anthropic
import openai

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from congruent.llm.manager import pm
from congruent.llm.service import LLMService
from congruent.schemas.completion import CompletionRequest
from congruent.schemas.message import Message

load_dotenv()

pm.register_default_providers()
llm_openai = LLMService(client=openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"]))
llm_anthropic = LLMService(
    client=anthropic.Client(api_key=os.environ["ANTHROPIC_API_KEY"])
)


class AnonymizationResult(BaseModel):
    original: str
    anonymized: str
    replacements: str = Field(
        description="The replacements made during anonymization: ({original} -> {placeholder})",
    )


def anonymize_text(text: str) -> AnonymizationResult:
    messages = [
        Message(
            role="system",
            content="You are an expert at anonymizing text by replacing personal information with generic placeholders.",
        ),
        Message(role="user", content=f"Anonymize the following text: {text}"),
    ]
    request = CompletionRequest(
        model="gpt-4o-mini",
        response_format=AnonymizationResult,
        messages=messages,
    )
    result = llm_openai.get_completion(request)
    return result


if __name__ == "__main__":
    original_text = "John Doe, born on 05/15/1980, lives at 123 Main St, New York. His email is john.doe@example.com."

    result = anonymize_text(original_text)

    print(f"Original: {result.parsed.original}")
    print(f"Anonymized: {result.parsed.anonymized}")
    print(f"Replacements: {result.parsed.replacements}")
