from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=10)
    gender = models.CharField(max_length=2)
    age = models.IntegerField()

    def __str__(self):
        return self.name


class Instance(models.Model):
    """
    ip: instance ip
    status: true is online and false is offline
    server_port: running port of agent client in client host
    last_update_time: last time of health check
    """
    ip = models.CharField(max_length=15)
    status = models.BooleanField()
    server_port = models.IntegerField()
    last_update_time = models.DateTimeField(auto_now=True)

