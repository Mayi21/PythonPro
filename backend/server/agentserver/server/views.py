import subprocess

from apscheduler.jobstores.base import JobLookupError
from apscheduler.triggers.interval import IntervalTrigger
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import requests
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from .models import User, Instance
from .service import get_command_res



from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

# 实例化调度器
scheduler = BackgroundScheduler()
# 调度器使用默认的DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), 'default')

def health_monitor():
    instances = Instance.objects.all()
    for ins in instances:
        health_check_url = "http://{}:{}/health".format(ins.ip, ins.server_port)
        print(health_check_url)
        resp = requests.get(health_check_url)
        print(resp.status_code)
        if resp.status_code == 200:
            ins.status = True
            ins.save()


# schedule_job = scheduler.get_job('health_check', DjangoJobStore())
# print(schedule_job.name)
# if schedule_job:
try:
    scheduler.remove_job('health_check')
    scheduler.add_job(health_monitor,
                      trigger=IntervalTrigger(seconds=5),
                      id='health_check',
                      name='health___check')
except JobLookupError:
    scheduler.add_job(health_monitor,
                      trigger=IntervalTrigger(seconds=5),
                      id='health_check',
                      name='health___check')


def index(request):
    return render(request, "index.html", {})

@csrf_exempt
def get_cmd_res(request):
    get_command_res(request)
