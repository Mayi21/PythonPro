from pydantic import BaseModel


class Cmd(BaseModel):
    name: str
    description: str
    value: str


class ContainerId(BaseModel):
    value: str


class PortItem(BaseModel):
    vm_port: str
    pm_port: str
    pm_ip: str
