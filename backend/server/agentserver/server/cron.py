import datetime

from django_cron import CronJobBase, Schedule
import requests

from backend.server.agentserver.server.models import Instance



# get data from database
def __get_instance_info():
    instances = Instance.objects.all()
    for ins in instances:
        health_check_url = "{}:{}/health".format(ins.ip, ins.server_port)
        resp = requests.get(health_check_url)
        if resp.status_code == 200:
            ins.status = True
            ins.save()



class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # 1分钟运行一次

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'server.health_monitor'

    def do(self):
        instances = Instance.objects.all()
        for ins in instances:
            health_check_url = "{}:{}/health".format(ins.ip, ins.server_port)
            resp = requests.get(health_check_url)
            if resp.status_code == 200:
                ins.status = True
                ins.save()

