import abc

from typing import Dict, List, Optional

from clipped.config.schema import BaseSchemaModel


class Tool(BaseSchemaModel):
    _USE_DISCRIMINATOR = True

    name: str
    description: Optional[str] = None
    args: List[str]
    inputs: List[Dict]
    outputs: List[Dict]
    tags: Optional[List[str]] = None
    verbose: Optional[bool] = None

    @abc.abstractmethod
    def _run(**kwrags) -> str:
        raise NotImplementedError()
