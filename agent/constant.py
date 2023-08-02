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

class DockerCMD(Enum):
    PULL_VM = ""
    RUN_VM = "docker run -d -p"
    STOP_VM = "docker stop"
    DEL_VM = "docker container rm"
    GET_IP = "docker inspect -f \'{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}\'"