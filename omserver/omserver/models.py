from django.db import models

# Create your models here.

class AgentInfo(models.Model):
    """
    存储Agent信息的模型
    """
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=255, verbose_name='IP地址')
    sn = models.CharField(max_length=255, verbose_name='设备SN')
    updateTime = models.BigIntegerField(verbose_name='更新时间戳')

    class Meta:
        db_table = 'agent_info'  # 设置数据库表名
        verbose_name = 'Agent信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"Agent(IP: {self.ip}, SN: {self.sn})"