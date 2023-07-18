# Generated by Django 4.2.3 on 2023-07-18 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_instance'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstanceMetric',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('disk_usgae', models.IntegerField()),
                ('cpu_usage', models.IntegerField()),
                ('ip', models.CharField(db_index=True, max_length=15)),
                ('collect_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
