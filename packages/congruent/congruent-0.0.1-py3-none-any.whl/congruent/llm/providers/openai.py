from typing import Any, Dict, List, Literal, Optional, T, Union

from congruent.llm.hookspecs import hookimpl
from congruent.llm.providers.utils import convert_to_openai_function
from congruent.schemas.completion import CompletionRequest, CompletionResponse


def _handle_tools(
    obj: type[T],
    strict: Optional[bool] = None,
) -> Dict:
    kwargs = {}
    obj_schema = convert_to_openai_function(obj, strict=strict)
    kwargs["tools"] = [
        {
            "type": "function",
            "function": obj_schema,
        }
    ]
    kwargs["tool_choice"] = {
        "type": "function",
        "function": {"name": obj_schema["name"]},
    }
    return kwargs


def _format_message_content(content: Union[Dict[str, Any], str]) -> Dict[str, Any]:
    """Format attachment for OpenAI API"""
    if not isinstance(content, dict):
        return {"type": "text", "text": str(content)}

    # Handle image attachments
    if content.get("type") == "image_url":
        return content

    # Handle audio attachments
    elif content.get("type") == "input_audio":
        audio_data = content["input_audio"]
        return {
            "type": "input_audio",
            "input_audio": {
                "data": audio_data["data"],
                "format": audio_data.get("format", "mp3"),
            },
        }

    return content


def _prepare_messages(request: CompletionRequest) -> List[Dict[str, Any]]:
    messages = []
    for msg in request.messages:
        if isinstance(msg.content, str):
            messages.append({"role": msg.role, "content": msg.content})
        else:
            messages.append(
                {
                    "role": msg.role,
                    "content": [_format_message_content(item) for item in msg.content],
                }
            )
    return messages


def _prepare_kwargs(request: CompletionRequest) -> Dict[str, Any]:
    kwargs = {}
    if request.tools:
        if not request.mode or request.mode == "tools":
            kwargs = _handle_tools(request.tools[0])
        elif request.mode == "json":
            kwargs["response_format"] = {
                "type": "json_object",
                "schema": convert_to_openai_function(request.tools[0]),
            }
    elif request.response_format:
        kwargs["response_format"] = request.response_format
        kwargs["parse"] = True
    elif request.mode == "json":
        kwargs["response_format"] = {"type": "json_object"}

    if request.stop:
        kwargs["stop"] = request.stop
    if request.temperature:
        kwargs["temperature"] = request.temperature
    if request.max_tokens:
        kwargs["max_tokens"] = request.max_tokens
    return kwargs


def _prepare_response(request: CompletionRequest, response: Any) -> CompletionResponse:
    tool_calls = response.choices[0].message.tool_calls if request.tools else None
    content = response.choices[0].message.content
    parsed = (
        response.choices[0].message.parsed
        if hasattr(response.choices[0].message, "parsed")
        else None
    )
    return CompletionResponse(
        content=content,
        parsed=parsed,
        tool_calls=tool_calls,
        model=request.model,
        provider="openai",
        usage={
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
        raw_response=response.model_dump(),
    )


@hookimpl
def get_completion(client, request: CompletionRequest) -> CompletionResponse:
    messages = _prepare_messages(request)

    oai_fct = client.chat.completions.create
    kwargs = _prepare_kwargs(request)
    if kwargs.pop("parse", False):
        oai_fct = client.beta.chat.completions.parse

    response = oai_fct(model=request.model, messages=messages, **kwargs)

    return _prepare_response(request, response)


@hookimpl
async def get_completion_async(
    client, request: CompletionRequest
) -> CompletionResponse:
    messages = _prepare_messages(request)

    oai_fct = client.chat.completions.create
    kwargs = _prepare_kwargs(request)
    if kwargs.pop("parse", False):
        oai_fct = client.beta.chat.completions.parse

    response = await oai_fct(model=request.model, messages=messages, **kwargs)

    return _prepare_response(request, response)


@hookimpl
def validate_client(client) -> Optional[Literal["openai"]]:
    if client.__class__.__name__ in {
        "OpenAI",
        "AsyncOpenAI",
    }:
        return "openai"


@hookimpl
def handle_function(
    obj: type[T],
) -> Dict:
    return _handle_tools(obj)
