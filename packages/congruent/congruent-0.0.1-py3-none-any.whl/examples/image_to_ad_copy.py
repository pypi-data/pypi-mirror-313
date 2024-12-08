import logging
import os

from typing import List, Optional

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


logger = logging.getLogger(__name__)


class Product(BaseModel):
    """
    Represents a product extracted from an image using AI.

    The product attributes are dynamically determined based on the content
    of the image and the AI's interpretation. This class serves as a structured
    representation of the identified product characteristics.
    """

    name: str = Field(
        description="A generic name for the product.", example="Headphones"
    )
    key_features: Optional[List[str]] = Field(
        description="A list of key features of the product that stand out.",
        default=None,
    )

    description: Optional[str] = Field(
        description="A description of the product.",
        default=None,
    )

    # Can be customized and automatically generated
    def generate_prompt(self):
        prompt = f"Product: {self.name}\n"
        if self.description:
            prompt += f"Description: {self.description}\n"
        if self.key_features:
            prompt += f"Key Features: {', '.join(self.key_features)}\n"
        return prompt


class IdentifiedProduct(BaseModel):
    """
    Represents a list of products identified in the images.
    """

    products: Optional[List[Product]] = Field(
        description="A list of products identified by the AI.",
        example=[
            Product(
                name="Headphones",
                description="Wireless headphones with noise cancellation.",
                key_features=["Wireless", "Noise Cancellation"],
            )
        ],
        default=None,
    )

    error: bool = Field(
        description="Indicates if there was an error during product identification",
        default=None,
    )
    message: Optional[str] = Field(
        description="Error message if applicable", default=None
    )


class AdCopy(BaseModel):
    """
    Represents a generated ad copy.
    """

    headline: str = Field(
        description="A short, catchy, and memorable headline for the given product. The headline should invoke curiosity and interest in the product.",
    )
    ad_copy: str = Field(
        description="A long-form advertisement copy for the given product. This will be used in campaigns to promote the product with a persuasive message and a call-to-action with the objective of driving sales.",
    )
    name: str = Field(description="The name of the product being advertised.")


def read_images(image_urls: list[str]) -> IdentifiedProduct:
    """
    Given a list of image URLs, identify the products in the images.
    """

    logger.info(f"Identifying products in images... {len(image_urls)} images")

    request = CompletionRequest(
        model="gpt-4o-mini",
        response_format=IdentifiedProduct,
        mode="json",
        max_tokens=1024,  # can be changed
        temperature=0,
        messages=[
            Message(
                role="user",
                content=[
                    {
                        "type": "text",
                        "text": "Identify products using the given images and generate key features for each product.",
                    },
                    *[
                        {"type": "image_url", "image_url": {"url": url}}
                        for url in image_urls
                    ],
                ],
            )
        ],
    )
    return llm_openai.get_completion(request).parsed


def generate_ad_copy(product: Product) -> AdCopy:
    """
    Given a product, generate an ad copy for the product.
    """

    logger.info(f"Generating ad copy for product: {product.name}")

    request = CompletionRequest(
        model="gpt-4o-mini",
        response_format=AdCopy,
        mode="json",
        temperature=0.3,
        messages=[
            Message(
                role="system",
                content="You are an expert marketing assistant for all products. Your task is to generate an advertisement copy for a product using the name, description, and key features.",
            ),
            Message(
                role="user",
                content=product.generate_prompt(),
            ),
        ],
    )
    return llm_openai.get_completion(request).parsed


data = [
    "https://contents.mediadecathlon.com/p1279823/9a1c59ad97a4084a346c014740ae4d3ff860ea70b485ee65f34017ff5e9ae5f7/recreational-ice-skates-fit-50-black.jpg?format=auto",
    "https://contents.mediadecathlon.com/p1279822/a730505231dbd6747c14ee93e8f89e824d3fa2a5b885ec26de8d7feb5626638a/recreational-ice-skates-fit-50-black.jpg?format=auto",
    "https://contents.mediadecathlon.com/p2329893/1ed75517602a5e00245b89ab6a1c6be6d8968a5a227c932b10599f857f3ed4cd/mens-hiking-leather-boots-sh-100-x-warm.jpg?format=auto",
    "https://contents.mediadecathlon.com/p2047870/8712c55568dd9928c83b19c6a4067bf161811a469433dc89244f0ff96a50e3e9/men-s-winter-hiking-boots-sh-100-x-warm-grey.jpg?format=auto",
]

for url in data:
    product = read_images([url])
    ad_copy = generate_ad_copy(product.products[0])
    print(ad_copy)
