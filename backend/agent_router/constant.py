from enum import Enum


class KafkaInfo(Enum):
    COMMAND_TOPIC = "server_command"
    RES_TOPIC = "client_res"
