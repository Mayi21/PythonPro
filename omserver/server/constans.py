from enum import Enum

class TaskState(Enum):
    READY = 'ready'
    PROCESSING = 'processing'
    FINISHED = 'finished'
    ERROR = 'error'