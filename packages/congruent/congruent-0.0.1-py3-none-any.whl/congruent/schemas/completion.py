from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from congruent.schemas.message import Message


class CompletionRequest(BaseModel):
    messages: List[Message]
    model: str
    mode: Optional[Literal["tools", "json"]] = Field(default="tools")
    tools: Optional[List[Any]] = None
    response_format: Optional[Any] = None
    temperature: Optional[float] = Field(default=0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=None, gt=0)
    stop: Optional[List[str]] = None


class CompletionResponse(BaseModel):
    content: Optional[str] = None
    tool_calls: Optional[List[Any]] = None
    parsed: Optional[Any] = None
    model: str
    provider: str
    usage: Dict[str, int]
    raw_response: Dict[str, Any]
