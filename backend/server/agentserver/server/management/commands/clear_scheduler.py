from django.core.management.base import BaseCommand
from django_apscheduler.models import DjangoJob, DjangoJobExecution

class Command(BaseCommand):
    help = 'Clears scheduler tasks from the database'

    def handle(self, *args, **options):
        # 清除任务信息的逻辑
        DjangoJobExecution.objects.all().delete()
        DjangoJob.objects.all().delete()  # 根据实际情况修改模型和条件

        self.stdout.write(self.style.SUCCESS('Scheduler tasks cleared successfully'))