from pydantic import BaseModel

from .function import Function


class ToolCall(BaseModel):
    id: str
    function: Function
    type: str
