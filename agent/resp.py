import json

from constant import RequestInfo


class Response:
    code: RequestInfo
    msg: str

    def __init__(self, code: RequestInfo.SUCCESS_CODE, msg: str, data):
        self.code = code
        self.msg = msg
        self.data = json.loads(data)
