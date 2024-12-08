import os

from typing import Iterable, List, Literal

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


class Query(BaseModel):
    """Class representing a single question in a query plan."""

    id: int = Field(..., description="Unique id of the query")
    question: str = Field(
        ...,
        description="Question asked using a question answering system",
    )
    dependencies: List[int] = Field(
        default_factory=list,
        description="List of sub questions that need to be answered before asking this question",
    )
    node_type: Literal["SINGLE", "MERGE_MULTIPLE_RESPONSES"] = Field(
        default="SINGLE",
        description="Type of question, either a single question or a multi-question merge",
    )


class QueryPlan(BaseModel):
    """Container class representing a tree of questions to ask a question answering system."""

    query_graph: List[Query] = Field(
        ..., description="The query graph representing the plan"
    )

    def _dependencies(self, ids: List[int]) -> List[Query]:
        """Returns the dependencies of a query given their ids."""
        return [q for q in self.query_graph if q.id in ids]


def query_planner(question: str) -> QueryPlan:
    messages = [
        Message(
            role="system",
            content="You are a world class query planning algorithm capable of breaking apart questions into its dependency queries such that the answers can be used to inform the parent question. Do not answer the questions, simply provide a correct compute graph with good specific questions to ask and relevant dependencies. Before you call the function, think step-by-step to get a better understanding of the problem.",
        ),
        Message(
            role="user",
            content=f"Consider: {question}\nGenerate the correct query plan.",
        ),
    ]

    request = CompletionRequest(
        model="gpt-4o-mini",
        temperature=0,
        response_format=QueryPlan,
        mode="json",
        messages=messages,
        max_tokens=1000,
    )
    return llm_openai.get_completion(request).parsed


plan = query_planner(
    "What is the difference in populations of Canada and the Jason's home country?"
)
for query in plan.query_graph:
    print(query)
