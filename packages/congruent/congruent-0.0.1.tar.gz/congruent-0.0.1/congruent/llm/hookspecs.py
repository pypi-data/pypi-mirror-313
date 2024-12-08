from typing import Any, Dict, Optional, T

import pluggy

from congruent.schemas.completion import CompletionRequest, CompletionResponse

# Define the plugin hook specification
hookspec = pluggy.HookspecMarker("llm_interface")
hookimpl = pluggy.HookimplMarker("llm_interface")


@hookspec
def validate_client(client: Any) -> Optional[str]:
    """Validate if the client is supported by this provider."""


@hookspec
def get_completion(client: Any, request: CompletionRequest) -> CompletionResponse:
    """Get a completion from the provider."""


@hookspec
async def get_completion_async(
    client: Any, request: CompletionRequest
) -> CompletionResponse:
    """Get a completion from the provider asynchronously."""


@hookspec
def handle_function(
    obj: type[T],
) -> Dict:
    """Handle a function and return the response."""
