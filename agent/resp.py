from constant import RespCode


class Response:
    code: RespCode
    msg: str

    def __init__(self, code: RespCode.SUCCESS_CODE, msg: str):
        self.code = code
        self.msg = msg
