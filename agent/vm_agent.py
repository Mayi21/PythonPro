import os

from fastapi import UploadFile, File
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
import logging
from logging.handlers import TimedRotatingFileHandler

from resp import Response

# 创建 TimedRotatingFileHandler
log_handler = TimedRotatingFileHandler('vm_agent_app.log', when='midnight', interval=1, backupCount=14)
log_handler.setLevel(logging.INFO)

# 创建 Formatter
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)

# 添加 Handler 到根日志记录器
logging.root.addHandler(log_handler)

from utils import __exec_cmd
from models import *
from utils import *
from constant import InstanceEnv
import socket

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

# get env parameter
PM_IP = os.getenv("PM_IP")
PM_PORT = os.getenv("PM_PORT")
SERVER = os.getenv("SERVER")


# health api
@app.get("/health")
async def get_info():
    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)
    return {"status": 200, "hostname": hostname, "ip": ip}


@app.on_event("startup")
def register_info():
    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)

    deploy_host_url = "http://{}/register-info/".format(SERVER)
    data = {
        'type': "VM",
        'vm_ip': ip,
        'pm_ip': PM_IP,
        'pm_port': PM_PORT,
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


# execute shell command
@app.post("/cmd")
async def run_cmd(command: Cmd):
    print("execute shell cmd is {}".format(command.value))
    out = __exec_cmd(command.value)
    return Response(RequestInfo.SUCCESS_CODE,
                    msg="execute cmd success",
                    data=out)


# execute shell script
@app.get("/exec-shell")
async def execute_shell_file(file_name: str):
    print("execute shell file is {}".format(file_name))
    shell_file_path = os.path.join(InstanceEnv.PLUGIN_SCRIPT_PATH.value, file_name)
    return __exec_cmd('sh ' + shell_file_path)['result']


# upload shell script
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
