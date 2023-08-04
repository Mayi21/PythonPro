from pydantic import BaseModel


class Cmd(BaseModel):
    name: str
    description: str
    value: str


class ContainerId(BaseModel):
    value: str


class PortItem(BaseModel):
    value: str
