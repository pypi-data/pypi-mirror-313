from __future__ import annotations

from typing import Literal
from typing import TypeVar

import openai
from loguru import logger
from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.parsed_chat_completion import ParsedChatCompletion
from pydantic import BaseModel

from .client import get_openai_client
from .settings import get_settings
from .types import BaseTool
from .types import Message

ResponseFormatT = TypeVar("ResponseFormatT", bound=BaseModel)


class Chat:
    def __init__(self, tools: list[type[BaseTool]] | None = None) -> None:
        logger.debug("Initializing Chat with tools: {}", tools)
        self.client = get_openai_client()
        self.messages: list[Message] = []
        self.tools = {tool.__name__: tool for tool in tools} if tools else {}
        self.settings = get_settings()

    def _create(self, response_format: type[ResponseFormatT] | None = None) -> ChatCompletion | ParsedChatCompletion:
        logger.debug("Creating chat completion with response_format: {}", response_format)

        kwargs = {
            "messages": [m.model_dump() for m in self.messages],
            "model": self.settings.openai_model,
            "temperature": self.settings.openai_temperature,
        }
        if self.tools:
            kwargs["tools"] = [openai.pydantic_function_tool(tool) for tool in self.tools.values()]

        if response_format:
            kwargs["response_format"] = response_format

        if self.settings.openai_max_tokens:
            kwargs["max_tokens"] = self.settings.openai_max_tokens

        response: ChatCompletion | ParsedChatCompletion
        if response_format:
            response = self.client.beta.chat.completions.parse(**kwargs)  # type: ignore
        else:
            response = self.client.chat.completions.create(**kwargs)  # type: ignore

        logger.debug("Chat completion created: {}", response)
        return response

    def _handle_response(
        self,
        response: ChatCompletion | ParsedChatCompletion,
        response_format: type[ResponseFormatT] | None = None,
    ):
        logger.debug("Handling response: {}", response)
        if not self.tools:
            return response

        if not response.choices:
            return response

        finish_reason = response.choices[0].finish_reason
        logger.debug("Finish reason: {}", finish_reason)
        if finish_reason != "tool_calls":
            return response

        self.add_assistant_message(response.choices[0].message)

        tool_calls = response.choices[0].message.tool_calls
        if not tool_calls:
            return response

        for tool_call in tool_calls:
            tool = self.tools.get(tool_call.function.name)
            if not tool:
                continue

            logger.debug("Calling tool: {}", tool_call.function.name)
            function_result = tool.call(tool_call.function.arguments)
            self.add_tool_message(function_result, tool_call.id)

        return self._create(response_format=response_format)

    def add_message(self, content: str, role: Literal["system", "user"] = "user") -> None:
        logger.debug("Adding message with content: {} and role: {}", content, role)
        match role:
            case "user":
                self.add_user_message(content)
            case "system":
                self.add_system_message(content)
            case _:
                raise ValueError(f"Invalid role: {role}")

    def add_assistant_message(self, message: ChatCompletionMessage) -> None:
        self.messages += [Message.model_validate(message.model_dump(exclude_none=True))]

    def add_user_message(self, content: str) -> None:
        logger.debug("Adding user message with content: {}", content)
        self.messages += [Message(content=content, role="user")]

    def add_system_message(self, content: str) -> None:
        logger.debug("Adding system message with content: {}", content)
        self.messages += [Message(content=content, role="system")]

    def add_tool_message(self, content: str, tool_call_id: str) -> None:
        logger.debug("Adding tool message with content: {} and tool_call_id: {}", content, tool_call_id)
        self.messages += [Message(content=content, role="tool", tool_call_id=tool_call_id)]

    def dump_messages(self) -> list[dict]:
        return [m.model_dump() for m in self.messages]

    def load_messages(self, messages: list[dict]) -> None:
        self.messages = [Message.model_validate(m) for m in messages]

    def create(self, response_format: type[ResponseFormatT] | None = None) -> ResponseFormatT | str:
        logger.debug("Creating final response with response_format: {}", response_format)
        response = self._handle_response(self._create(response_format), response_format)
        if not response.choices:
            raise ValueError("No completion choices returned")

        response_message = response.choices[0].message
        self.messages += [response_message]

        if response_format:
            if not response_message.parsed:
                raise ValueError("No completion parsed content returned")
            return response_message.parsed

        if not response_message.content:
            raise ValueError("No completion content returned")
        return response_message.content
