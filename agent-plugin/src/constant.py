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


class DockerCMD(Enum):
    PULL_VM = ""
    RUN_VM = "docker run -d -p"
    STOP_VM = "docker stop"
    START_VM = "docker start"
    DEL_VM = "docker container rm"
    GET_IP = "docker inspect -f \'{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}\'"
    GET_RUNNING_VM = "docker ps"
    GET_VM_PORT = "docker port"
