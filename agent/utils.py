import json
import os
import subprocess

from agent.constant import RequestInfo


def __exec_cmd(cmd):
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        result = output.decode().strip() if output else error.decode().strip()
        return {"result": result}
    except Exception as e:
        return {"result": str(e)}


def check_shell_file(file_name):
    pass


def get_config():
    with open('config.json') as f:
        config = json.load(f)
    return config


class HttpUtil():
    def __init__(self, url):
        self.url = url
        pass

    def post(self, data, headers: RequestInfo.REQ_HEADERS):
        pass

    def get(self):
        pass


if __name__ == '__main__':
    print(get_config())
