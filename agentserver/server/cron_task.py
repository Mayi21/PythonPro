import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore
from .models import *
from .constant import *
from .utils import *

# 实例化调度器
scheduler = BackgroundScheduler()
# 调度器使用默认的DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), 'default')

http_util = HttpUtil()


# cron health check
def health_monitor():
    host_status_records = HostStatusRecord.objects.exclude(status=DeployHostStatus.OFFLINE.value).exclude(status=DeployHostStatus.STOP.value)
    for ins in host_status_records:
        # TODO test use local host
        # production use vm ip
        health_check_url = "http://{}:{}/health".format('127.0.0.1', ins.port)
        print(health_check_url)
        resp = http_util.req(RequestInfo.METHOD_GET,
                      health_check_url,
                      data=None)
        print(resp.content, resp.status_code)
        if resp.status_code == 200:
            ins.status = DeployHostStatus.ONLINE.value
        else:
            ins.status = DeployHostStatus.UNKNOWN.value
        ins.save()


scheduler.add_job(health_monitor,
                  trigger=IntervalTrigger(seconds=60),
                  )
