import json
import os

from fastapi import UploadFile, File
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from models import *
from resp import Response
from utils import __exec_cmd
from constant import InstanceEnv, RequestInfo, DockerCMD

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


# run container
@app.post("/deploy-host")
async def deploy_host(port_item: PortItem):
    vm_port = port_item.vm_port
    pm_ip = port_item.pm_ip
    pm_port = port_item.pm_port
    out = __exec_cmd('{} {}:8000 --name agent_{} agent'.format(DockerCMD.RUN_VM.value,
                                                               vm_port,
                                                               vm_port))
    if len(out['result']) != 64:
        return Response(RequestInfo.INTERNAL_ERROR,
                        msg="deploy host fail, cause by {}".format(out['result']))
    container_ip = __exec_cmd('{} {}'.format(DockerCMD.GET_IP.value,
                                             out['result']))
    return Response(RequestInfo.SUCCESS_CODE,
                    msg=json.dumps({'container_id': out['result'],
                                    'ip': container_ip['result']}))


# stop host
@app.post("/stop-host")
async def stop_host(container_id: ContainerId):
    container_id = container_id.value
    out = __exec_cmd('{} {}'.format(DockerCMD.STOP_VM.value,
                                    container_id))
    if len(out['result']) != len(container_id):
        return Response(RequestInfo.INTERNAL_ERROR,
                        msg="deploy host fail, cause by {}".format(out['result']))
    return Response(RequestInfo.SUCCESS_CODE,
                    msg=out['result'])


# delete host
@app.delete('/del-host')
async def del_host(container_id: ContainerId):
    container_id = container_id.value
    out = __exec_cmd('{} {}'.format(DockerCMD.DEL_VM.value,
                                    container_id))
    if len(out['result']) != len(container_id):
        return Response(RequestInfo.INTERNAL_ERROR,
                        msg="deploy host fail, cause by {}".format(out['result']))
    return Response(RequestInfo.SUCCESS_CODE,
                    msg=out['result'])


def sync_vm_info():
    out = __exec_cmd(DockerCMD.GET_RUNNING_VM.value)['result']
    out = out.split("\n")
    if len(out) == 1:
        return
    vm_infos = []
    for info in out[1:]:
        id = info[:12]
        out = __exec_cmd("{} {}".format(DockerCMD.GET_VM_PORT.value,
                                        id))['result']
        port = out.split("->")[-1].split(":")[-1]
        vm_infos.append({'id': id,
                         'port': port})

    return vm_infos


def set_config_json(pm_ip, pm_port):
    try:
        config_json_path = "config.json"
        with open(config_json_path, 'r') as f:
            data = json.load(f)
        with open(config_json_path, "w+") as f:
            data['pm_ip'] = pm_ip
            data['pm_port'] = pm_port
            json.dump(data, f)
    except Exception as e:
        raise e


if __name__ == '__main__':
    os.system('uvicorn pm_agent:app --reload')
