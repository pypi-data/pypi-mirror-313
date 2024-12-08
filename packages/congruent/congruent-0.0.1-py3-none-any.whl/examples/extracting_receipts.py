import os

from typing import List

import anthropic
import openai

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationInfo, model_validator

from congruent.llm.manager import pm
from congruent.llm.service import LLMService
from congruent.schemas.completion import CompletionRequest, Message

load_dotenv()

pm.register_default_providers()
llm_openai = LLMService(client=openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"]))
llm_anthropic = LLMService(
    client=anthropic.Client(api_key=os.environ["ANTHROPIC_API_KEY"])
)


class Item(BaseModel):
    name: str
    price: float
    quantity: int


class Receipt(BaseModel):
    items: list[Item]
    total: float

    @model_validator(mode="after")
    def check_total(self):
        items = self.items
        total = self.total
        calculated_total = sum(item.price * item.quantity for item in items)
        if abs(calculated_total - total) > 0.01:
            raise ValueError(
                f"Total {total} does not match the sum of item prices {calculated_total}"
            )
        return self


def extract(url: str) -> Receipt:
    messages = [
        Message(
            role="user",
            content=[
                {
                    "type": "image_url",
                    "image_url": {"url": url},
                },
                {
                    "type": "text",
                    "text": "Analyze the image and return the items in the receipt and the total amount.",
                },
            ],
        )
    ]
    request = CompletionRequest(
        model="gpt-4o-2024-08-06",
        response_format=Receipt,
        mode="json",
        messages=messages,
        max_tokens=4000,
    )
    return llm_openai.get_completion(request)


url = "https://templates.mediamodifier.com/645124ff36ed2f5227cbf871/supermarket-receipt-template.jpg"


receipt = extract(url)
print(receipt)
