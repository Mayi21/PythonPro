import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore

from backend.server.agentserver.server.models import Instance

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
