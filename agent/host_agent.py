import os
import subprocess

from fastapi import UploadFile, File
from fastapi import Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from agent.utils import __exec_cmd
from constant import InstanceEnv

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


class Cmd(BaseModel):
    name: str
    description: str
    value: str

# health api
@app.get("/health")
async def get_info():
    import socket

    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)
    return {"status": 200, "hostname": hostname, "ip": ip}

# execute shell command
@app.post("/cmd")
async def run_cmd(command: Cmd):
    return __exec_cmd(command.value)

# execute shell script
@app.get("/exec-shell")
async def execute_shell_file(file_name: str):
    shell_file_path = os.path.join(InstanceEnv.PLUGIN_SCRIPT_PATH.value, file_name)
    return __exec_cmd('sh ' + shell_file_path)

# upload shell script
@app.post('/uploadfiles')
@limiter.limit("10/second")
async def upload_shell_file(request: Request, file: UploadFile=File(...)):
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

# run container
@app.post("/deploy-host")
async def deploy_host(port: str):
    out = __exec_cmd('docker run -d -p {}:8000 --name agent_{} agent'.format(port, port))
    if len(out['result']) != 64:
        return {'error': out['result']}
    return {'success': out['result']}

@app.post("/stop-host")
async def stop_host(container_id: str):
    out = __exec_cmd('docker stop {}'.format(container_id))
    if len(out['result']) != 64:
        return {'error': out['result']}
    return {'success': out['result']}

@app.post('/del-host')
async def del_host(container_id: str):
    out = __exec_cmd('docker container rm {}'.format(container_id))
    if len(out['result']) != 64:
        return {'error': out['result']}
    return {'success': out['result']}



if __name__ == '__main__':
    os.system('uvicorn agent_server:app --reload')
