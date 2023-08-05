# Generated by Django 4.2.3 on 2023-08-05 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeployHostRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('vm_id', models.CharField(max_length=64)),
                ('ip', models.CharField(max_length=15)),
                ('port', models.CharField(max_length=6)),
                ('vm_name', models.CharField(max_length=100)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('pm_ip', models.CharField(max_length=15)),
                ('pm_port', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'deploy_host_record',
            },
        ),
        migrations.CreateModel(
            name='HostRegisterInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('host_type', models.CharField(max_length=2)),
                ('vm_ip', models.CharField(max_length=15)),
                ('pm_ip', models.CharField(max_length=15)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'host_register_info',
            },
        ),
        migrations.CreateModel(
            name='HostStatusRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('vm_id', models.CharField(max_length=64)),
                ('ip', models.CharField(max_length=15)),
                ('port', models.CharField(max_length=6)),
                ('vm_name', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=10)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('pm_ip', models.CharField(max_length=15)),
                ('pm_port', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'host_status_record',
            },
        ),
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=15)),
                ('status', models.BooleanField()),
                ('server_port', models.IntegerField()),
                ('hostname', models.CharField(max_length=30)),
                ('container_id', models.CharField(max_length=64)),
                ('last_update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='InstanceMetric',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('disk_usage', models.IntegerField()),
                ('cpu_usage', models.IntegerField()),
                ('ip', models.CharField(db_index=True, max_length=15)),
                ('collect_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'instance_metrics',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('gender', models.CharField(max_length=2)),
                ('age', models.IntegerField()),
            ],
        ),
    ]
