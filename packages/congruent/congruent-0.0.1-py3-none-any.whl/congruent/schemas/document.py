import numpy as np

from typing import Any, Dict, List, Optional, Union

from clipped.config.schema import BaseSchemaModel


class Document(BaseSchemaModel):
    id: str
    content: Any
    metadata: Dict[str, Any]
    embedding: Optional[Union[list[float], np.ndarray]] = None
    tags: Optional[List[str]] = None
    order: Optional[int] = None
    tokens: Optional[int] = None
