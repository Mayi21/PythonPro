import json

from django.db import models

# Create your models here.

class AgentInfo(models.Model):
    """
    存储Agent信息的模型
    """
    ip = models.CharField(max_length=255, verbose_name='IP地址')
    sn = models.CharField(max_length=255, verbose_name='设备SN')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'agent_info'  # 设置数据库表名
        verbose_name = 'Agent信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"Agent(IP: {self.ip}, SN: {self.sn})"

class InstallTask(models.Model):
    """
    存储安装插件任务详情
    """

    ip = models.CharField(max_length=255, verbose_name='IP地址')
    sn = models.CharField(max_length=255, verbose_name='设备SN')
    passwd = models.CharField(max_length=255, verbose_name='主机密码')
    state = models.CharField(max_length=20, verbose_name='状态')
    info = models.TextField(verbose_name='详情')
    create_time = models.DateTimeField(auto_now_add = True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'install_task'  # 设置数据库表名
        verbose_name = '安装任务信息'
        verbose_name_plural = verbose_name

    def to_json(self):
        data = {
            'id': self.id,
            'ip': self.ip,
            'sn': self.sn,
            'passwd': self.passwd,
            'state': self.state,
            'info': self.info,
            'create_time': str(self.create_time),
            'update_time': str(self.update_time)
        }
        return data

