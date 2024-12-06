from typing import Literal

from pydantic import BaseModel

from .toolcall import ToolCall


class Message(BaseModel):
    role: Literal["system", "user", "tool", "assistant"]
    content: str | None = None
    tool_call_id: str | None = None
    tool_calls: list[ToolCall] | None = None
