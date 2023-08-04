from enum import Enum


class KafkaInfo(Enum):
    COMMAND_TOPIC = "server_command"
    RES_TOPIC = "client_res"


class InstanceEnv(Enum):
    PLUGIN_SCRIPT_PATH = "/opt/plugin"
    PLUGIN_TEMP_PATH = '/tmp'

class RequestInfo(Enum):
    SUCCESS_CODE = "200"
    INTERNAL_ERROR = "500"
    REQ_HEADERS = {'Content-Type': 'application/json'}
    METHOD_GET = "GET"
    METHOD_POST = "POST"
    METHOD_DELETE = "DELETE"
    METHOD_PUT = "PUT"

class DeployHostStatus(Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    STOP = "STOP"

class HostType(Enum):
    VM = "VM"
    PM = "PM"

class HostInfo(Enum):
    pass

