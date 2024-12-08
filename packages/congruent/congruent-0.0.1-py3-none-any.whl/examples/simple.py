import os

import anthropic
import openai

from dotenv import load_dotenv

from congruent.llm.manager import pm
from congruent.llm.service import LLMService
from congruent.schemas.completion import CompletionRequest
from congruent.schemas.message import Message

load_dotenv()

SYSTEM_PROMPT = """You are a precise multi-label classification system.
Respond in the following JSON format:
{
    "labels": [
        {"name": "label_name", "category": "category_name", "confidence": 0.95}
    ]
}
Ensure confidence scores are between 0 and 1."""


def main():
    print("Running main")
    llm_openai = LLMService(client=openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"]))
    llm_anthropic = LLMService(
        client=anthropic.Client(api_key=os.environ["ANTHROPIC_API_KEY"])
    )

    # Create a openai request
    request = CompletionRequest(
        messages=[Message(role="user", content="Hello, how are you?")],
        model="gpt-4",
        temperature=0.7,
        max_tokens=50,
    )

    # Get completion
    response = llm_openai.get_completion(request)
    print("+-+" * 10)
    print(f"Response from {response.provider} ({response.model}): {response.content}")
    print("+-+" * 10)

    # Create a claude request
    request = CompletionRequest(
        messages=[Message(role="user", content="Hello, how are you?")],
        model="claude-3-5-sonnet-20241022",
        temperature=0.7,
        max_tokens=50,
    )

    # Get completion
    response = llm_anthropic.get_completion(request)
    print("+-+" * 10)
    print(f"Response from {response.provider} ({response.model}): {response.content}")
    print("+-+" * 10)


if __name__ == "__main__":
    pm.register_default_providers()
    main()
