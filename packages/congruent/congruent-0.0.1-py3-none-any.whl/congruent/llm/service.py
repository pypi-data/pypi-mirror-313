from typing import Any, Literal

from clipped.compact.pydantic import PrivateAttr
from clipped.config.schema import BaseSchemaModel

from congruent.llm.exceptions import ModelNotSupportedError
from congruent.llm.manager import pm
from congruent.schemas.completion import CompletionRequest, CompletionResponse


class LLMService(BaseSchemaModel):
    client: Any
    _provider: Literal["openai", "anthropic"] = PrivateAttr()

    def __init__(
        self,
        **data,
    ):
        super().__init__(**data)
        self._validate_client()

    def _validate_client(self):
        for result in pm.hook.validate_client(client=self.client):
            if result:
                self._provider = result
                return
        raise ModelNotSupportedError("Client does not match any known LLM provider.")

    def get_completion(self, request: CompletionRequest) -> CompletionResponse:
        """Get a completion from the appropriate LLM provider."""
        # Get implementations for specific provider only
        impl = pm.get_plugins().get(self._provider)
        if not impl:
            raise ModelNotSupportedError(
                f"No implementation found for provider {self._provider}"
            )
        return impl.get_completion(client=self.client, request=request)

    async def get_completion_async(
        self, request: CompletionRequest
    ) -> CompletionResponse:
        """Get a completion from the appropriate LLM provider asynchronously."""
        impl = pm.get_plugins().get(self._provider)
        if not impl:
            raise ModelNotSupportedError(
                f"No implementation found for provider {self._provider}"
            )
        return await impl.get_completion_async(client=self.client, request=request)
