from typing import Any, Dict, List, Literal, Optional, T, Type, Union

from congruent.llm.hookspecs import hookimpl
from congruent.llm.providers.utils import convert_to_openai_function
from congruent.schemas.completion import CompletionRequest, CompletionResponse


def _handle_tools(
    obj: Type[T],
    strict: Optional[bool] = None,
) -> Dict:
    """Convert tools to Anthropic's format"""
    kwargs = {}
    openai_schema = convert_to_openai_function(obj, strict=strict)

    # Convert from OpenAI format to Anthropic format
    tool = {
        "name": openai_schema["name"],
        "description": openai_schema["description"],
        "input_schema": openai_schema["parameters"],
    }

    kwargs["tools"] = [tool]
    return kwargs


def _format_message_content(content: Union[Dict[str, Any], str]) -> Dict[str, Any]:
    """Format attachment for Anthropic API"""
    if not isinstance(content, dict):
        return {"type": "text", "text": str(content)}

    # Handle image attachments
    if content.get("type") == "image_url":
        url = content["image_url"]["url"]
        if url.startswith("data:"):
            # Handle base64 images
            media_type = url.split(";")[0].split(":")[1]
            data = url.split(",")[1]
            return {
                "type": "image",
                "source": {"type": "base64", "media_type": media_type, "data": data},
            }
        else:
            # Convert URL images to base64
            import base64
            import requests

            response = requests.get(url)
            data = base64.b64encode(response.content).decode()
            return {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": response.headers["Content-Type"],
                    "data": data,
                },
            }

    # Handle audio attachments - Anthropic doesn't support audio yet
    elif content.get("type") == "input_audio":
        raise NotImplementedError("Audio attachments are not supported by Anthropic")

    return content


def _validate_role(role: str) -> str:
    if role == "system":
        return "assistant"
    return role


def _prepare_messages(request: CompletionRequest) -> List[Dict[str, Any]]:
    # Convert messages to Anthropic format, handling attachments
    messages = []
    for msg in request.messages:
        if isinstance(msg.content, str):
            messages.append({"role": _validate_role(msg.role), "content": msg.content})
        else:
            # Format each content item
            content = [_format_message_content(item) for item in msg.content]
            messages.append({"role": _validate_role(msg.role), "content": content})
    return messages


def _prepare_kwargs(request: CompletionRequest) -> Dict[str, Any]:
    kwargs = {}
    if request.tools:
        if not request.mode or request.mode == "tools":
            kwargs = _handle_tools(request.tools[0])
        elif request.mode == "json":
            # TODO: For JSON mode, we use a single tool with tool_choice to force its use
            kwargs = _handle_tools(request.tools[0])
            kwargs["tool_choice"] = {"type": "tool", "name": kwargs["tools"][0]["name"]}

    if request.stop:
        kwargs["stop"] = request.stop
    if request.temperature:
        kwargs["temperature"] = request.temperature
    if request.max_tokens:
        kwargs["max_tokens"] = request.max_tokens
    return kwargs


def _prepare_response(request: CompletionRequest, response: Any) -> CompletionResponse:
    content = next((c.text for c in response.content if c.type == "text"), None)
    tool_calls = next((c for c in response.content if c.type == "tool_use"), None)
    return CompletionResponse(
        content=content,
        tool_calls=tool_calls,
        model=request.model,
        provider="anthropic",
        usage={
            "prompt_tokens": response.usage.input_tokens,
            "completion_tokens": response.usage.output_tokens,
            "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
        },
        raw_response=response.model_dump(),
    )


@hookimpl
def get_completion(client, request: CompletionRequest) -> CompletionResponse:
    messages = _prepare_messages(request)
    kwargs = _prepare_kwargs(request)

    response = client.messages.create(model=request.model, messages=messages, **kwargs)
    return _prepare_response(request, response)


@hookimpl
async def get_completion_async(
    client, request: CompletionRequest
) -> CompletionResponse:
    messages = _prepare_messages(request)
    kwargs = _prepare_kwargs(request)
    response = await client.messages.create(
        model=request.model, messages=messages, **kwargs
    )

    return _prepare_response(request, response)


@hookimpl
def validate_client(client) -> Optional[Literal["anthropic"]]:
    if client.__class__.__name__ in {
        "Anthropic",
        "AsyncAnthropic",
    }:
        return "anthropic"
