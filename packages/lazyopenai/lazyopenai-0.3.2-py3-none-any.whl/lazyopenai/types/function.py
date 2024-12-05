from pydantic import BaseModel


class Function(BaseModel):
    arguments: str
    name: str
