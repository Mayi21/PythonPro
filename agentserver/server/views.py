import threading

import paramiko
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from .service import *


# index page
def index(request):
    return render(request, "index.html", {})


# get result of execute command
@csrf_exempt
def get_cmd_res(request):
    return get_command_res(request)


@csrf_exempt
def get_instance_metric(request):
    return get_instance_metrics(request)


# get upload page view
def upload_plugin_page(reuqest):
    return render(reuqest, "UploadPlugin.html", {})


# deploy host
@csrf_exempt
def deploy_host_func(request):
    return deploy_host()


@csrf_exempt
def start_host_func(request):
    return start_host(request)


# stop host
@csrf_exempt
def stop_host_func(request):
    return stop_host(request)


# delete host
@csrf_exempt
def del_host_func(request):
    return del_host(request)


# host manage page
def host_management_page(request):
    return render(request, "DeployHost.html", {})


# get deploy host info
def get_deploy_host_info_info(request):
    return get_deploy_host_func(request)


def make_fake_data(request):
    thread = threading.Thread(target=test_generate_fake_date)
    thread.start()
    return JsonResponse({'status': "success"})


@csrf_exempt
def register_info_func(request):
    return register_info_collect(request)


@csrf_exempt
def sync_vm_info_func(request):
    request.body

    pass


@csrf_exempt
def execute_sync_cmd_function(request):
    """
    request:
        ip/uuid: 唯一标识一台机器
        cmd: 需要执行的命令

    """
    data = json.loads(request.body)
    ip = data['ip']
    uuid = data['uuid']
    cmd = data['cmd']
    if ip is None and uuid is None:
        return JsonResponse("ip or uuid is null!", status=400)


# 用户输入节点IP、root密码后，通过在agent server上远程登录到对应主机安装agent client，
# 同时将server服务节点信息写入到主机上，完成agent client服务启动
@csrf_exempt
def install_agent(request):
    rq_body = json.loads(request.body)
    host_ip = rq_body['host_ip']
    host_pwd = rq_body['host_pwd']
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=host_ip, port=22, username='root', password=host_pwd)

    # TODO 执行安装命令
    # TODO 执行文件内容写入
    stdin, stdout, stderr = ssh.exec_command('df')
    # 获取命令结果
    result = stdout.read()
    print(result.decode('utf-8'))
    # 关闭连接
    ssh.close()
