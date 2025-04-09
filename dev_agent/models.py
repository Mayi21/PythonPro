from pydantic import BaseModel


class Cmd(BaseModel):
    name: str
    description: str
    value: str


class VMId(BaseModel):
    value: str


class PortItem(BaseModel):
    vm_port: str
    pm_port: str
    pm_ip: str


class VMIds(BaseModel):
    datas: list
