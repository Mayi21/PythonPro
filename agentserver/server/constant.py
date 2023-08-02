from enum import Enum


class KafkaInfo(Enum):
    COMMAND_TOPIC = "server_command"
    RES_TOPIC = "client_res"


class InstanceEnv(Enum):
    PLUGIN_SCRIPT_PATH = "/opt/plugin"
    PLUGIN_TEMP_PATH = '/tmp'

class RespCode(Enum):
    SUCCESS_CODE = "200"
    INTERNAL_ERROR = "500"
