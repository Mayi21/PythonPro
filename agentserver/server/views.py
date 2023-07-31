import json
import threading

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from .service import (get_command_res,
                      get_instance_metrics,
                      test_generate_fake_date,
                      deploy_host,
                      get_deploy_host_func)


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

