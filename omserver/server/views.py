# dashboard/views.py
import json
import threading
import time
import uuid

import paramiko
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

from .constans import TaskState
from .models import AgentInfo, InstallTask

NODES = [
    {'name': 'Node1', 'url': 'http://node1_ip:5000'},
    {'name': 'Node2', 'url': 'http://node2_ip:5000'},
]

@api_view(['GET'])
def node_list(request):
    return Response(NODES)

@api_view(['GET'])
def node_detail(request, node_name):
    node = next((n for n in NODES if n['name'] == node_name), None)
    if not node:
        return Response({'error': 'Node not found'}, status=404)
    try:
        response = requests.get(f"{node['url']}/system_info", timeout=5)
        return Response(response.json())
    except requests.RequestException as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def execute_command(request, node_name):
    node = next((n for n in NODES if n['name'] == node_name), None)
    if not node:
        return Response({'error': 'Node not found'}, status=404)
    command = request.data.get('command')
    if not command:
        return Response({'error': 'No command provided'}, status=400)
    try:
        response = requests.post(f"{node['url']}/execute_command", json={'command': command}, timeout=10)
        return Response(response.json())
    except requests.RequestException as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def upload_file(request, node_name):
    node = next((n for n in NODES if n['name'] == node_name), None)
    if not node:
        return Response({'error': 'Node not found'}, status=404)
    data = request.data
    required_fields = ['local_path', 'remote_path', 'hostname', 'username', 'password']
    if not all(field in data for field in required_fields):
        return Response({'error': 'Missing required fields'}, status=400)
    try:
        response = requests.post(f"{node['url']}/upload_file", json=data, timeout=10)
        return Response(response.json())
    except requests.RequestException as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def update_vm_info(request):
    data = json.loads(request.body)
    if 'node_ip' not in data:
        return Response({'error': 'Missing required fields'}, status=400)
    if 'node_sn' not in data:
        return Response({'error': 'Missing required fields'}, status=400)
    node_ip = data['node_ip']
    node_sn = data['node_sn']
    _, created = AgentInfo.objects.update_or_create(ip=node_ip, sn=node_sn)
    if created:
        return Response({'INFO': 'Created new record!'}, status=200)
    else:
        return Response({'INFO': 'Updated existing record!'}, status=200)

@api_view(['GET'])
def get_task_info(request, task_id: str):
    task_info = InstallTask.objects.get(id=task_id)
    return Response({'data': task_info.to_json()}, status=200)

def install_rpm(task_id: str, ip: str, passwd: str, sn: str):
    install_task = InstallTask.objects.get(id=task_id)
    wget_url = "http://192.168.100.157/myrepo/packages/agent-plugin-1.0.0-1.el7.noarch.rpm"  # 可选参数，默认给个链接
    install_task.state = TaskState.PROCESSING.value
    update_install_task_info(install_task, "Start connect node.")
    install_task.save()

    try:
        # 建立 SSH 连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        update_install_task_info(install_task, "Start connect node.")
        ssh.connect(hostname=ip, username='root', password=passwd)

        # 执行安装命令
        install_rpm_cmd = "rpm -ivh {}".format(wget_url)
        update_install_task_info(install_task, "Execute command {}".format(install_rpm_cmd))
        stdin, stdout, stderr = ssh.exec_command(install_rpm_cmd)
        output = stdout.read().decode()
        error = stderr.read().decode()
        update_install_task_info(install_task, "Output {}".format(output))

        # 执行内容替换命令
        replace_conf_cmd = "sed -i 's/SERVER_IP/{}/g; s/SN/{}/g' /usr/local/agent/conf/agent.conf".format('192.168.0.110', sn)

        update_install_task_info(install_task, "Execute command {}".format(replace_conf_cmd))
        stdin, stdout, stderr = ssh.exec_command(replace_conf_cmd)
        output = stdout.read().decode()
        error = stderr.read().decode()
        update_install_task_info(install_task, "Output {}".format(output))

        # 执行服务启动命令
        start_app_cmd = "bash /usr/local/agent/bin/agent-start start"
        update_install_task_info(install_task, "Execute command {}".format(start_app_cmd))
        stdin, stdout, stderr = ssh.exec_command(start_app_cmd)
        output = stdout.read().decode()
        error = stderr.read().decode()
        update_install_task_info(install_task, "Output {}".format(output))
        ssh.close()
    except Exception as e:
        return Response({'error': str(e)}, status=500)

def update_install_task_info(task: InstallTask, new_info: str):
    task.info = task.info + "\n" + get_time_now() + " " + new_info
    task.save()


def get_time_now():
    # 获取当前时间戳
    import time

    timestamp = time.time()
    local_time = time.localtime(timestamp)
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    return formatted_time

@api_view(['POST'])
def deploy_vm(request):
    """
    接收参数后通过 root 登录远程服务器，并执行 wget 命令
    """
    data = json.loads(request.body)
    if "ip" not in data:
        return Response({'error': 'Missing required fields'}, status=400)
    if "passwd" not in data:
        return Response({'error': 'Missing required fields'}, status=400)
    ip = data["ip"]
    passwd = data["passwd"]
    vm_sn = uuid.uuid4()

    install_task = InstallTask(
        ip=ip,
        sn=vm_sn,
        passwd=passwd,
        state=TaskState.READY.value,
    )
    install_task.save()
    resp = {
        'task_id': install_task.id,
    }
    thread = threading.Thread(target=install_rpm, args=(install_task.id, ip, passwd, vm_sn))
    thread.start()
    return Response({'data': json.dumps(resp)}, status=200)

