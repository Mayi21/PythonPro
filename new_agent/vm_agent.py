import os
import threading
from enum import Enum
from fastapi import UploadFile, File
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
import logging
from logging.handlers import TimedRotatingFileHandler
import socket
import json
import subprocess
import requests
import uuid


class RequestInfo(Enum):
    SUCCESS_CODE = "200"
    INTERNAL_ERROR = "500"
    REQ_HEADERS = {'Content-Type': 'application/json'}
    METHOD_GET = "GET"
    METHOD_POST = "POST"
    METHOD_DELETE = "DELETE"
    METHOD_PUT = "PUT"


class InstanceEnv(Enum):
    PLUGIN_SCRIPT_PATH = "/opt/plugin"
    PLUGIN_TEMP_PATH = '/tmp'


class Cmd(BaseModel):
    name: str
    description: str
    value: str


# execute shell command
def __exec_cmd(cmd):
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        result = output.decode().strip() if output else error.decode().strip()
        return {"result": result}
    except Exception as e:
        return {"result": str(e)}


# 异步执行命令
def async_exec_cmd(cmd):
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        result = output.decode().strip() if output else error.decode().strip()
        # 返回到kafka消息中
        return {"result": result}
    except Exception as e:
        return {"result": str(e)}


# 同步执行命令
def sync_exec_cmd(cmd):
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        result = output.decode().strip() if output else error.decode().strip()
        return {"result": result}
    except Exception as e:
        return {"result": str(e)}


def get_uuid():
    return str(uuid.uuid4())


class HttpUtil:

    def __post(self, url, data, headers):
        resp = requests.post(url=url,
                             data=data,
                             headers=headers)
        return resp

    def __get(self, url, data, params, headers):
        resp = requests.get(url=url,
                            data=data,
                            params=params,
                            headers=headers)
        return resp

    def __put(self, url, data, params, headers):
        resp = requests.put(url=url,
                            data=data,
                            params=params,
                            headers=headers)
        return resp

    def __delete(self, url, data, params, headers):
        resp = requests.delete(url=url,
                               params=params,
                               data=data,
                               headers=headers)
        return resp

    def req(self, method: RequestInfo, url: str, data, params, headers=RequestInfo.REQ_HEADERS.value):
        data = json.dumps(data)
        if method == RequestInfo.METHOD_GET:
            return self.__get(url=url, data=data, params=params, headers=headers)
        elif method == RequestInfo.METHOD_PUT:
            return self.__put(url=url, data=data, params=params, headers=headers)
        elif method == RequestInfo.METHOD_POST:
            return self.__post(url=url, data=data, headers=headers)
        else:
            return self.__delete(url=url, data=data, params=params, headers=headers)


class Response:
    code: RequestInfo
    msg: str

    def __init__(self, code: RequestInfo.SUCCESS_CODE, msg: str, data):
        self.code = code
        self.msg = msg
        self.data = json.loads(data)


# 创建 TimedRotatingFileHandler
log_handler = TimedRotatingFileHandler('../agent-plugin/logs/vm_agent_app.log', when='midnight', interval=1, backupCount=14)
log_handler.setLevel(logging.INFO)

# 创建 Formatter
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)

# 添加 Handler 到根日志记录器
logging.root.addHandler(log_handler)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
origins = [
    "http://127.0.0.1:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

req_util = HttpUtil()


# health api
@app.get("/health")
async def get_info():
    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)
    return {"status": 200, "hostname": hostname, "ip": ip}


# 服务启动执行的任务
# 在服务启动是，获取本地配置的agent server服务端信息，上报消息到server上
# 上报的内容是当前时间+
@app.on_event("startup")
def register_info():
    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)

    uuid_id = uuid.uuid4()

    with open('../agent-plugin/conf/agent.conf', 'r') as f:
        agent_server_config = json.load(f)

    deploy_host_url = "http://{}:{}/register-info/".format(agent_server_config['SERVER'], agent_server_config['PORT'])
    data = {
        'type': "VM",
        'vm_ip': ip,
        'vm_name': hostname
    }
    print(data)
    resp = req_util.req(RequestInfo.METHOD_POST,
                        deploy_host_url,
                        data,
                        None)

    if resp.status_code == 200 and json.loads(resp.content)['status'] == 200:
        print("register success")
    elif resp.status_code == 200:
        print(json.loads(resp.content)['msg'])
    else:
        print("network error")


# 异步执行shell命令，将执行结果返回大kafka中消费
# 目前是将kafka消息中加上节点IP和命令，来让调用方区分那个节点的那个命令的返回内容是
@app.post("/v2/async-cmd")
async def async_execute_cmd(command: Cmd):
    print("execute shell cmd is {}".format(command.value))
    # 开启一个线程，用来执行异步命令，然后将结果返回到kafka中
    exec_cmd_thread = threading.Thread(target=async_exec_cmd(command.value))
    exec_cmd_thread.start()
    return Response(RequestInfo.SUCCESS_CODE,
                    msg="execute cmd success",
                    data=None)


# 同步执行shell命令，在接口中返回响应结果
@app.post("/v2/sync-cmd/")
async def sync_execute_cmd(command: Cmd):
    print("execute shell cmd is {}".format(command.value))
    out = sync_exec_cmd(command.value)
    return Response(RequestInfo.SUCCESS_CODE,
                    msg="execute cmd success",
                    data=out)


# execute shell script
@app.get("/exec-shell")
async def execute_shell_file(file_name: str):
    print("execute shell file is {}".format(file_name))
    shell_file_path = os.path.join(InstanceEnv.PLUGIN_SCRIPT_PATH.value, file_name)
    return __exec_cmd('sh ' + shell_file_path)['result']


# 上传shell脚本
# 限制上传的大小和文件后缀
# 将上传后的shell脚本文件放在本地
@app.post('/uploadfiles')
@limiter.limit("10/second")
async def upload_shell_file(request: Request, file: UploadFile = File(...)):
    # need a front page that
    file_data = file.file.read()
    if file.size / 1024 >= 1024:
        return {'error': 'file size to large, upload max size is 1MB'}
    file_name = file.filename
    if not file_name.endswith(".sh"):
        return {'error': '{} file format can\'t support'.format(file_name.split(".")[-1])}
    des_file = os.path.join(InstanceEnv.PLUGIN_TEMP_PATH.value, file_name)
    with open(des_file, 'wb') as f:
        f.write(file_data)
    return {"success": file.filename}


if __name__ == '__main__':
    os.system('uvicorn vm_agent:app --reload')
