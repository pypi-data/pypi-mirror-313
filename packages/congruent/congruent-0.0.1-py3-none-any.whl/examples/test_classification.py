import os

import anthropic
import openai

from dotenv import load_dotenv

from congruent.llm.manager import pm
from congruent.llm.service import LLMService
from congruent.schemas.completion import CompletionRequest, Message

load_dotenv()

from typing import List, Literal

from pydantic import BaseModel, Field


class ClassificationResponse(BaseModel):
    """
    A few-shot example of text classification:

    Examples:
    - "Buy cheap watches now!": SPAM
    - "Meeting at 3 PM in the conference room": NOT_SPAM
    - "You've won a free iPhone! Click here": SPAM
    - "Can you pick up some milk on your way home?": NOT_SPAM
    - "Increase your followers by 10000 overnight!": SPAM
    """

    chain_of_thought: str = Field(
        ...,
        description="The chain of thought that led to the prediction.",
    )
    label: Literal["SPAM", "NOT_SPAM"] = Field(
        ...,
        description="The predicted class label.",
    )


class MultiClassPrediction(BaseModel):
    """
    Class for a multi-class label prediction.

    Examples:
    - "My account is locked": ["TECH_ISSUE"]
    - "I can't access my billing info": ["TECH_ISSUE", "BILLING"]
    - "When do you close for holidays?": ["GENERAL_QUERY"]
    - "My payment didn't go through and now I can't log in": ["BILLING", "TECH_ISSUE"]
    """

    chain_of_thought: str = Field(
        ...,
        description="The chain of thought that led to the prediction.",
    )

    class_labels: List[Literal["TECH_ISSUE", "BILLING", "GENERAL_QUERY"]] = Field(
        ...,
        description="The predicted class labels for the support ticket.",
    )


pm.register_default_providers()
llm_openai = LLMService(client=openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"]))
llm_anthropic = LLMService(
    client=anthropic.Client(api_key=os.environ["ANTHROPIC_API_KEY"])
)


def main_text_classification():
    prompt = "Classify the following text: <text>{data}</text>"
    tests = [
        ("Hey Jason! You're awesome", "NOT_SPAM"),
        ("I am a nigerian prince and I need your help.", "SPAM"),
    ]

    # OpenAI
    for text, label in tests:
        request = CompletionRequest(
            messages=[Message(role="user", content=prompt.format(data=text))],
            tools=[ClassificationResponse],
            model="gpt-4o-2024-08-06",
            temperature=0.7,
            max_tokens=50,
        )

        response = llm_openai.get_completion(request)
        print("+-+" * 10)
        print(f"Original text: {text}, label: {label}")
        print(
            f"Response from {response.provider} ({response.model}): {response.tool_calls}"
        )
        print("+-+" * 10)

    # Anthropic
    for text, label in tests:
        request = CompletionRequest(
            messages=[Message(role="user", content=prompt.format(data=text))],
            tools=[ClassificationResponse],
            model="claude-3-5-sonnet-20241022",
            temperature=0.7,
            max_tokens=100,
        )
        response = llm_anthropic.get_completion(request)
        print("+-+" * 10)
        print(f"Original text: {text}, label: {label}")
        print(
            f"Response from {response.provider} ({response.model}): {response.tool_calls}"
        )
        print("+-+" * 10)


def main_multi_class_classification():
    prompt = "Classify the following support ticket: <ticket>{data}</ticket>"
    tests = [
        ("My account is locked", ["TECH_ISSUE"]),
        ("I can't access my billing info", ["TECH_ISSUE", "BILLING"]),
        ("When do you close for holidays?", ["GENERAL_QUERY"]),
        (
            "My payment didn't go through and now I can't log in",
            ["BILLING", "TECH_ISSUE"],
        ),
        (
            "My account is locked and I can't access my billing info.",
            ["TECH_ISSUE", "BILLING"],
        ),
    ]

    # OpenAI
    for ticket, labels in tests:
        request = CompletionRequest(
            messages=[Message(role="user", content=prompt.format(data=ticket))],
            tools=[MultiClassPrediction],
            model="gpt-4o-2024-08-06",
            temperature=0.7,
            max_tokens=500,
        )

        response = llm_openai.get_completion(request)
        print("+-+" * 10)
        print(f"Original ticket: {ticket}, labels: {labels}")
        print(
            f"Response from {response.provider} ({response.model}): {response.tool_calls}"
        )
        print("+-+" * 10)

    # Anthropic
    for ticket, labels in tests:
        request = CompletionRequest(
            messages=[Message(role="user", content=prompt.format(data=ticket))],
            tools=[MultiClassPrediction],
            model="claude-3-5-sonnet-20241022",
            temperature=0.7,
            max_tokens=500,
        )
        response = llm_anthropic.get_completion(request)
        print("+-+" * 10)
        print(f"Original ticket: {ticket}, labels: {labels}")
        print(
            f"Response from {response.provider} ({response.model}): {response.tool_calls}"
        )
        print("+-+" * 10)


if __name__ == "__main__":
    print("Running text classification")
    main_text_classification()
    print("Running multi-class classification")
    main_multi_class_classification()
