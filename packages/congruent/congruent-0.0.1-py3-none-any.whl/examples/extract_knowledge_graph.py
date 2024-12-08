import os

from typing import List

import anthropic
import openai

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationInfo, model_validator

from congruent.llm.manager import pm
from congruent.llm.service import LLMService
from congruent.schemas.completion import CompletionRequest, Message


class Node(BaseModel, frozen=True):
    id: int
    label: str
    color: str


class Edge(BaseModel, frozen=True):
    source: int
    target: int
    label: str
    color: str = "black"


class KnowledgeGraph(BaseModel):
    nodes: List[Node] = Field(..., default_factory=list)
    edges: List[Edge] = Field(..., default_factory=list)


load_dotenv()

pm.register_default_providers()
llm_openai = LLMService(client=openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"]))
llm_anthropic = LLMService(
    client=anthropic.Client(api_key=os.environ["ANTHROPIC_API_KEY"])
)

from graphviz import Digraph


def visualize_knowledge_graph(kg: KnowledgeGraph):
    dot = Digraph(comment="Knowledge Graph")

    # Add nodes
    for node in kg.nodes:
        dot.node(str(node.id), node.label, color=node.color)

    # Add edges
    for edge in kg.edges:
        dot.edge(str(edge.source), str(edge.target), label=edge.label, color=edge.color)

    # Render the graph
    dot.render("knowledge_graph.gv", view=True)


def main():
    question = "Teach me about quantum mechanics"

    messages = [
        Message(
            role="user",
            content=f"Help me understand the following by describing it as a detailed knowledge graph: {question}",
        ),
    ]

    request = CompletionRequest(
        messages=messages,
        model="gpt-4o-mini",
        tools=[KnowledgeGraph],
    )

    response = llm_openai.get_completion(request)
    print(response.tool_calls)

    kn = KnowledgeGraph.model_validate_json(response.tool_calls[0].function.arguments)
    visualize_knowledge_graph(kn)


if __name__ == "__main__":
    main()
