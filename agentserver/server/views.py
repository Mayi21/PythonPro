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




def make_fake_data(request):
    thread = threading.Thread(target=test_generate_fake_date)
    thread.start()
    return JsonResponse({'status': "success"})

