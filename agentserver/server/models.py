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
    hostname: container host name
    container id: use to stop container
    last_update_time: last time of health check
    """
    ip = models.CharField(max_length=15)
    status = models.BooleanField()
    server_port = models.IntegerField()
    hostname = models.CharField(max_length=30)
    container_id = models.CharField(max_length=64)
    last_update_time = models.DateTimeField(auto_now=True)

class DeployHost(models.Model):
    """
    deploy host table

    container_id: container id
    port: expose port
    create_time: container create time
    update_time: container update time

    """
    id = models.AutoField(primary_key=True)
    container_id = models.CharField(max_length=64)
    ip = models.CharField(max_length=15)
    port = models.CharField(max_length=6)
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)
    # online, offline, stop, exception
    status = models.CharField(max_length=15, default="ONLINE")
    host_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'deploy_host'


# include disk usage and cpu usage every 10 seconds
class InstanceMetric(models.Model):
    id = models.AutoField(primary_key=True)
    disk_usage = models.IntegerField()
    cpu_usage = models.IntegerField()
    ip = models.CharField(max_length=15, db_index=True)
    collect_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'instance_metrics'

class HostRegisterInfo(models.Model):
    id = models.AutoField(primary_key=True)
    host_type = models.CharField(max_length=2)
    vm_ip = models.CharField(max_length=15)
    pm_ip = models.CharField(max_length=15)
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'host_register_info'