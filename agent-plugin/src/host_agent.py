import json
import socket

import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import psutil
import subprocess
import platform
import os
import paramiko

app = FastAPI()
def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

def read_conf():
    """
    读取conf文件配置获取平台服务信息和sn信息
    """
    data = json.load(open("../conf/agent.conf", 'r'))
    return data['server_ip'], data['server_port'], data['sn']

server_ip, server_port, sn = read_conf()
host_ip = get_host_ip()



# 停止时，停止调度器
@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}


class SystemMonitor:
    def __init__(self):
        self.system_info = {}

    def get_cpu_info(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        self.system_info['cpu'] = {
            'usage_percent': cpu_percent,
            'cores': cpu_count,
            'logical_cores': psutil.cpu_count(logical=True)
        }
        return self.system_info['cpu']

    def get_memory_info(self):
        memory = psutil.virtual_memory()
        self.system_info['memory'] = {
            'total': f"{memory.total / (1024 ** 3):.2f} GB",
            'available': f"{memory.available / (1024 ** 3):.2f} GB",
            'percent': memory.percent
        }
        return self.system_info['memory']

    def get_disk_info(self):
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'total': f"{usage.total / (1024 ** 3):.2f} GB",
                    'used': f"{usage.used / (1024 ** 3):.2f} GB",
                    'free': f"{usage.free / (1024 ** 3):.2f} GB",
                    'percent': usage.percent
                })
            except:
                continue
        self.system_info['disk'] = disks
        return self.system_info['disk']

    def execute_command(self, command):
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            return {
                'output': result.stdout,
                'error': result.stderr,
                'return_code': result.returncode
            }
        except Exception as e:
            return {'error': str(e)}

    def execute_shell_script(self, script_path):
        if not os.path.exists(script_path):
            return {'error': 'Script file not found'}

        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ['cmd.exe', '/c', script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
            else:
                result = subprocess.run(
                    ['bash', script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
            return {
                'output': result.stdout,
                'error': result.stderr,
                'return_code': result.returncode
            }
        except Exception as e:
            return {'error': str(e)}

    def upload_file(self, local_path, remote_path, hostname, username, password, port=22):
        if not os.path.exists(local_path):
            return {'error': 'Local file not found'}
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, port, username, password)
            sftp = ssh.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            ssh.close()
            return {'status': 'success', 'message': f'File uploaded to {remote_path}'}
        except Exception as e:
            return {'error': str(e)}

    def get_system_summary(self):
        self.get_cpu_info()
        self.get_memory_info()
        self.get_disk_info()
        self.system_info['platform'] = {
            'system': platform.system(),
            'node': platform.node(),
            'release': platform.release(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return self.system_info


monitor = SystemMonitor()

# ===== Pydantic 请求体模型 =====
class CommandRequest(BaseModel):
    command: str

class ScriptRequest(BaseModel):
    script_path: str

class UploadRequest(BaseModel):
    local_path: str
    remote_path: str
    hostname: str
    username: str
    password: str
    port: Optional[int] = 22


# ===== API 路由 =====
@app.get("/system_info")
def get_system_info():
    return monitor.get_system_summary()


@app.post("/execute_command")
def run_command(req: CommandRequest):
    if not req.command:
        raise HTTPException(status_code=400, detail="No command provided")
    return monitor.execute_command(req.command)


@app.post("/execute_script")
def run_script(req: ScriptRequest):
    if not req.script_path:
        raise HTTPException(status_code=400, detail="No script path provided")
    return monitor.execute_shell_script(req.script_path)


@app.post("/upload_file")
def upload(req: UploadRequest):
    result = monitor.upload_file(
        local_path=req.local_path,
        remote_path=req.remote_path,
        hostname=req.hostname,
        username=req.username,
        password=req.password,
        port=req.port
    )
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@app.get("/health")
def health_check():
    return {"status": "healthy", "node": platform.node()}


def report_vm_info():
    '''
    请求平台地址注册主机信息
    '''
    req = {
        'node_ip': host_ip,
        'node_sn': sn
    }
    server_url = 'http://{}:{}{}'.format(server_ip, server_port, "/v2/api/register_node_info")
    resp = requests.post(server_url, data=json.dumps(req))
    print("update success")
# 创建调度器
scheduler = AsyncIOScheduler()

# 启动时，启动定时任务
@app.on_event("startup")
async def startup_event():
    scheduler.add_job(report_vm_info, IntervalTrigger(seconds=5))  # 每 5 秒执行一次
    scheduler.start()

