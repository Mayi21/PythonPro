from apscheduler.triggers.interval import IntervalTrigger
from django.http import HttpResponse
from django.shortcuts import render
import requests

# Create your views here.
from .models import User, Instance



def index(request):
    return HttpResponse("request path:{}".format(request.path))


def save_user(request):
    user = User(name='xiaohei', gender='m', age=10)
    user.save()
def get_user(request):
    data = User.objects.all()
    return HttpResponse(data)



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


scheduler.add_job(health_monitor,
                  trigger=IntervalTrigger(seconds=5),
                  id='health_check',
                  name='health check')


scheduler.start()
