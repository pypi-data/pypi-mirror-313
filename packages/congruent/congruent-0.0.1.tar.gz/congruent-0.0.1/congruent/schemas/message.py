import datetime

from typing import Any, Dict, List, Optional, Union
from typing_extensions import Literal

from clipped.compact.pydantic import Field
from clipped.config.schema import BaseSchemaModel

MessageRoles = Literal["system", "user", "assistant"]


class Message(BaseSchemaModel):
    content: Union[str, List[Dict[str, Any]]] = Field(
        description="Content of the message"
    )
    role: Optional[MessageRoles] = Field(
        description="Role of the message sender (e.g., 'user', 'assistant')",
        default=None,
    )
    created_at: Optional[datetime.datetime] = None
    user: Optional[str] = None
    tokens: Optional[int] = None
