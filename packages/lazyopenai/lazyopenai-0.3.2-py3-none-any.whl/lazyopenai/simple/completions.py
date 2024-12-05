import json
from typing import TypeVar

import openai
from pydantic import BaseModel

from ..client import get_openai_client
from ..settings import get_settings

T = TypeVar("T", bound=BaseModel)


def create(messages, tools: list[type[BaseModel]] | None = None) -> str:
    client = get_openai_client()
    settings = get_settings()

    tool_map = {tool.__name__: tool for tool in tools} if tools else {}

    kwargs = {"tools": [openai.pydantic_function_tool(tool) for tool in tools]} if tools else {}
    response = client.chat.completions.create(
        messages=messages,
        model=settings.openai_model,
        temperature=settings.openai_temperature,
        **kwargs,  # type: ignore
    )

    # handle tool calls
    if tools and response.choices:
        choice = response.choices[0]
        if choice.finish_reason == "tool_calls" and choice.message.tool_calls:
            tool_messages = []
            for tool_call in choice.message.tool_calls:
                tool = tool_map.get(tool_call.function.name)
                if not tool:
                    continue
                args = json.loads(tool_call.function.arguments)
                tool_messages.append(
                    {
                        "role": "tool",
                        "content": str(tool(**args)()),  # type: ignore
                        "tool_call_id": tool_call.id,
                    }
                )
            response = client.chat.completions.create(
                messages=messages + [choice.message] + tool_messages,
                model=settings.openai_model,
                temperature=settings.openai_temperature,
            )

    if not response.choices:
        raise ValueError("No completion choices returned")

    content = response.choices[0].message.content
    if not content:
        raise ValueError("No completion message content")

    return content


def parse(messages, response_format: type[T], tools: list[type[BaseModel]] | None = None) -> T:
    client = get_openai_client()
    settings = get_settings()

    tool_map = {tool.__name__: tool for tool in tools} if tools else {}

    kwargs = {"tools": [openai.pydantic_function_tool(tool) for tool in tools]} if tools else {}
    response = client.beta.chat.completions.parse(
        messages=messages,
        model=settings.openai_model,
        temperature=settings.openai_temperature,
        response_format=response_format,
        **kwargs,  # type: ignore
    )

    # handle tool calls
    if tools and response.choices:
        choice = response.choices[0]
        if choice.finish_reason == "tool_calls" and choice.message.tool_calls:
            tool_messages = []
            for tool_call in choice.message.tool_calls:
                tool = tool_map.get(tool_call.function.name)
                if not tool:
                    continue
                args = json.loads(tool_call.function.arguments)
                tool_messages.append(
                    {
                        "role": "tool",
                        "content": str(tool(**args)()),  # type: ignore
                        "tool_call_id": tool_call.id,
                    }
                )
            response = client.beta.chat.completions.parse(
                messages=messages + [choice.message] + tool_messages,
                model=settings.openai_model,
                temperature=settings.openai_temperature,
                response_format=response_format,
            )

    if not response.choices:
        raise ValueError("No completion choices returned")

    parsed = response.choices[0].message.parsed
    if not parsed:
        raise ValueError("No completion message parsed")

    return parsed
