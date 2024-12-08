from typing import Optional

from clipped.compact.pydantic import Field
from clipped.config.schema import BaseSchemaModel


class Agent(BaseSchemaModel):
    _USE_DISCRIMINATOR = True

    name: str = Field(description="The name of the agent")
    description: Optional[str] = Field(
        default=None,
        description="The description of the agent, visible to the user and other agents",
    )
    instructions: Optional[str] = Field(
        default="You are a helpful assistant, your goal is to be concise and helpful.",
        description="The instructions of the agent, private to the agent",
    )
