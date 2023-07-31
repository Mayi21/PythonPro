import json
import threading

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from .service import get_command_res, get_instance_metrics, test_generate_fake_date, deploy_host


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
def deploy_host_func(request):
    return deploy_host()


# host manage page
def host_management_page(request):
    return render(request, "DeployHost.html", {})

# get deploy host info
def get_deploy_host_info_info(request):
    instances = [
        {
            "id": 1,
            "ip": "127.0.0.1",
            "status": True,
            "server_port": 8000,
            "hostname": "container-1",
            "container_id": "1234567890abcdef",
            "last_update_time": "2023-07-28 12:00:00"
        },
        {
            "id": 2,
            "ip": "192.168.1.100",
            "status": True,
            "server_port": 9000,
            "hostname": "container-2",
            "container_id": "0987654321abcdef",
            "last_update_time": "2023-07-28 12:10:00"
        }
    ]
    serialized_instances = json.dumps(instances)  # 将非字典对象序列化为 JSON 格式的字符串
    return JsonResponse(serialized_instances, safe=False)  # 设置




def make_fake_data(request):
    thread = threading.Thread(target=test_generate_fake_date)
    thread.start()
    return JsonResponse({'status': "success"})

