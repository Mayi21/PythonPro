from constant import RequestInfo


class Response:
    code: RequestInfo
    msg: str

    def __init__(self, code: RequestInfo.SUCCESS_CODE, msg: str):
        self.code = code
        self.msg = msg
