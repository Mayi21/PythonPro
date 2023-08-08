from fastapi import UploadFile, File
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

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
PM_IP = os.getenv("pm_ip")
PM_PORT = os.getenv("pm_port")
SERVER = os.getenv("server")

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
    config = get_config()
    server = config['server']
    pm_ip = config['pm_ip']
    host_type = config['type']
    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)
    deploy_host_url = "http://{}/register-info/".format(server)
    data = {
        'type': host_type,
        'vm_ip': ip,
        'pm_ip': pm_ip,
    }
    resp = req_util.req(RequestInfo.METHOD_POST,
                        deploy_host_url,
                        data)

    if resp.status_code == 200 and json.loads(resp.content)['status'] == 200:
        print("register success")
    elif resp.status_code == 200:
        print(json.loads(resp.content)['msg'])
    else:
        print("network error")


# execute shell command
@app.post("/cmd")
async def run_cmd(command: Cmd):
    return __exec_cmd(command.value)['result']


# execute shell script
@app.get("/exec-shell")
async def execute_shell_file(file_name: str):
    shell_file_path = os.path.join(InstanceEnv.PLUGIN_SCRIPT_PATH.value, file_name)
    return __exec_cmd('sh ' + shell_file_path)['result']


# upload shell script
@app.post('/uploadfiles')
@limiter.limit("10/second")
async def upload_shell_file(request: Request, file: UploadFile = File(...)):
    # need a front page that
    file_data = file.file.read()
    if file.size / 1024 >= 1024:
        return {'error': 'shell script to large'}
    file_name = file.filename
    if not file_name.endswith(".sh"):
        return {'error': 'file check not match'}
    des_file = os.path.join(InstanceEnv.PLUGIN_SCRIPT_PATH.value, file_name)
    with open(des_file, 'wb') as f:
        f.write(file_data)
    return {"success": file.filename}


if __name__ == '__main__':
    os.system('uvicorn vm_agent:app --reload')
