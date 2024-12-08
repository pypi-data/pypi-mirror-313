import os

from typing import List

import anthropic
import openai

from dotenv import load_dotenv
from pydantic import BaseModel

from congruent.llm.manager import pm
from congruent.llm.service import LLMService
from congruent.schemas.completion import CompletionRequest, Message

load_dotenv()

pm.register_default_providers()
llm_openai = LLMService(client=openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"]))
llm_anthropic = LLMService(
    client=anthropic.Client(api_key=os.environ["ANTHROPIC_API_KEY"])
)


# Define Schemas for PII data
class Data(BaseModel):
    index: int
    data_type: str
    pii_value: str


class PIIDataExtraction(BaseModel):
    """
    Extracted PII data from a document, all data_types should try to have consistent property names
    """

    private_data: List[Data]

    def scrub_data(self, content: str) -> str:
        """
        Iterates over the private data and replaces the value with a placeholder in the form of
        <{data_type}_{i}>
        """
        for i, data in enumerate(self.private_data):
            content = content.replace(data.pii_value, f"<{data.data_type}_{i}>")
        return content


EXAMPLE_DOCUMENT = """
# Fake Document with PII for Testing PII Scrubbing Model
# (The content here)
"""

request = CompletionRequest(
    model="gpt-4o-mini",
    response_format=PIIDataExtraction,
    mode="json",
    messages=[
        Message(
            role="system",
            content="You are a world class PII scrubbing model, Extract the PII data from the following document",
        ),
        Message(
            role="user",
            content=EXAMPLE_DOCUMENT,
        ),
    ],
)  # type: ignore

pii_data = llm_openai.get_completion(request).parsed

print("Extracted PII Data:")
# > Extracted PII Data:
print(pii_data.model_dump_json())
"""
{"private_data":[{"index":0,"data_type":"Name","pii_value":"John Doe"},{"index":1,"data_type":"Email","pii_value":"john.doe@example.com"},{"index":2,"data_type":"Phone Number","pii_value":"(555) 123-4567"},{"index":3,"data_type":"Address","pii_value":"123 Main St, Anytown, USA"},{"index":4,"data_type":"Social Security Number","pii_value":"123-45-6789"}]}
"""
