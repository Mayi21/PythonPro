import json
import logging
import random
import subprocess
import time

from django.http import JsonResponse
from .utils import HttpUtil

from .models import *
from .constant import *

REQ_HEADERS = {'Content-Type': 'application/json'}

req_util = HttpUtil()


# input command and get execute result
def get_command_res(request):
    try:
        command = request.POST.get('cmd')
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        result = output.decode().strip() if output else error.decode().strip()
        return JsonResponse({"result": result})
    except Exception as e:
        return JsonResponse({"result": str(e)})


# get instance metrics info
def get_instance_metrics(request):
    data = json.loads(request.body)
    ip = data['ip']
    start_time = data['start_time']
    end_time = request.POST.get('end_time')
    results = InstanceMetric.objects.filter(ip=ip, collect_time__gte=start_time)
    resp = {'ip': ip}
    res_list = []
    for res in results:
        r = {'disk_usage': res.disk_usage,
             'cpu_usage': res.cpu_usage,
             'time': res.collect_time}
        res_list.append(r)
    resp.update({'data': res_list})
    return JsonResponse(resp)


def test_generate_fake_date():
    all_data = InstanceMetric.objects.all()
    all_data.delete()
    count = 60
    ips = ['205.218.217.155', '59.205.133.64', '88.202.177.174', '83.105.84.190', '32.166.44.66', '42.124.141.130',
           '29.13.249.233', '56.34.219.102', '112.171.37.7', '216.183.192.9', '31.208.40.173', '128.52.81.233',
           '39.171.135.227', '95.182.248.208', '181.90.1.217', '118.143.202.73', '242.226.242.119', '53.141.146.26',
           '224.207.136.150', '83.171.145.86', '33.15.118.31', '43.202.167.188', '163.106.67.41', '208.210.53.198',
           '67.216.248.173', '93.4.169.238', '192.221.90.9', '166.237.98.208', '170.238.27.183', '245.220.240.82',
           '134.113.5.79', '65.6.134.144', '147.70.117.51', '203.46.43.230', '238.170.192.237', '4.123.216.199',
           '181.235.206.43', '32.90.111.224', '239.177.11.127', '42.117.166.122', '168.182.30.84', '221.169.97.98',
           '125.97.238.107', '143.142.137.87', '100.161.237.29', '7.218.103.47', '241.61.99.118', '219.14.77.149',
           '87.167.115.45', '182.44.39.166', '240.105.119.25', '73.105.233.160', '17.83.231.155', '35.74.238.208',
           '161.232.213.79', '67.43.13.8', '155.23.204.4', '139.165.103.120', '19.234.22.210', '36.225.98.89',
           '209.238.85.195', '42.195.241.89', '137.220.133.149', '70.48.221.167', '16.240.168.56', '8.100.208.119',
           '120.240.151.130', '13.101.147.9', '237.145.83.143', '223.64.145.22', '125.235.151.58', '254.112.153.249',
           '177.10.251.207', '28.78.24.85', '111.162.237.162', '227.214.147.6', '96.114.151.125', '254.118.37.250',
           '120.115.191.71', '69.152.248.109', '89.61.21.190', '158.20.216.138', '54.227.87.43', '92.53.106.223',
           '143.199.42.3', '52.19.58.175', '244.201.64.39', '19.190.59.137', '153.18.53.205', '172.249.150.157',
           '86.22.215.83', '185.26.176.23', '222.149.189.31', '11.75.97.44', '215.226.180.82', '155.43.33.57',
           '93.123.126.140', '187.190.187.113', '191.185.25.56', "28.158.189.63'"]
    for i in range(1, count):
        for ip in ips:
            cpu_usage = random.randint(0, 200)
            disk_usage = random.randint(0, 100)
            instance_metrics = InstanceMetric(ip=ip,
                                              disk_usage=disk_usage,
                                              cpu_usage=cpu_usage)
            instance_metrics.save()
        time.sleep(1)


# get not use port to deploy container
## 1. select max port of online container then plus one
## 2. random generate and select by port if status eq false or not record
def __get_not_use_port():
    # 1. get have resource pm
    # 2. get ip from pm that not use
    # TODO default pm 127.0.0.1:8000, max number of host is 10

    pm_ip, pm_port, _ = __get_pm_info("")
    online_server_ports = (HostStatusRecord.objects.exclude(status=DeployHostStatus.OFFLINE.value)
                           .filter(pm_ip=pm_ip, pm_port=pm_port)
                           .values_list('port', flat=True))

    online_server_ports = set(online_server_ports)
    server_port = random.randint(49152, 65535)
    while server_port in online_server_ports:
        server_port = random.randint(49152, 65535)
    return server_port


def deploy_host():
    server_port = str(__get_not_use_port())
    logging.info("server port is ", server_port)
    print("server port is ", server_port)
    # TODO get host agent address
    pm_ip, pm_port, agent_address = __get_pm_info("")
    deploy_host_url = "{}/deploy-host".format(agent_address)
    resp = req_util.req(RequestInfo.METHOD_POST,
                        deploy_host_url,
                        {'vm_port': server_port,
                         "pm_ip": pm_ip,
                         "pm_port": pm_port})
    if resp.status_code == 200:
        msg = json.loads(resp.content)
        if msg['code'] == RequestInfo.SUCCESS_CODE.value:
            result = json.loads(msg['msg'])
            vm_id = result['container_id']
            vm_ip = result['ip']
            deploy_host_record: DeployHostRecord = DeployHostRecord(vm_id=vm_id,
                                                                    ip=vm_ip,
                                                                    port=server_port,
                                                                    pm_ip=pm_ip,
                                                                    pm_port=pm_port)
            deploy_host_record.save()
            return JsonResponse({'status': 200})
        else:
            return JsonResponse({'status': 500, 'msg': msg['msg']})
    else:
        return JsonResponse({'status': 500})


def start_host(request):
    container_id = json.loads(request.body)['id']
    if not container_id:
        return JsonResponse({'status': 500, "msg": "container id is empty"})
    pm_ip, pm_port, agent_address = __get_pm_info("")
    start_host_url = "{}/start-host".format(agent_address)
    resp = req_util.req(RequestInfo.METHOD_POST,
                        start_host_url,
                        {'value': container_id})
    if resp.status_code == 200:
        msg = json.loads(resp.content)
        if msg['code'] == RequestInfo.SUCCESS_CODE.value:
            # stop success
            print("start {} success".format(container_id))
            # 这里存在一个重复逻辑，启动容器后，会再次运行vm 服务，这个时候会再次上报信息到 host status record表中，而此时有刷新了，导致这个问题
            HostStatusRecord.objects.get(vm_id=container_id).delete()
            return JsonResponse({'status': 200, 'msg': 'start success'})
        else:
            # stop failure
            return JsonResponse({'status': 500, 'msg': msg['msg']})
    else:
        return JsonResponse({'status': 500, 'msg': str(resp.content)})


def stop_host(request):
    container_id = json.loads(request.body)['id']
    if not container_id:
        return JsonResponse({'status': 500, "msg": "container id is empty"})
    pm_ip, pm_port, agent_address = __get_pm_info("")
    stop_host_url = "{}/stop-host".format(agent_address)
    resp = req_util.req(RequestInfo.METHOD_POST,
                        stop_host_url,
                        {'value': container_id})
    if resp.status_code == 200:
        msg = json.loads(resp.content)
        if msg['code'] == RequestInfo.SUCCESS_CODE.value:
            # stop success
            print("stop {} success".format(container_id))
            host_status_record = HostStatusRecord.objects.get(vm_id=container_id)
            host_status_record.status = DeployHostStatus.STOP.value
            host_status_record.save()
            return JsonResponse({'status': 200, 'msg': 'stop success'})
        else:
            # stop failure
            return JsonResponse({'status': 500, 'msg': msg['msg']})
    else:
        return JsonResponse({'status': 500, 'msg': str(resp.content)})


# delete host
def del_host(request):
    container_id = json.loads(request.body)['id']
    if not container_id:
        return JsonResponse({'status': 500, "msg": "container id is empty"})
    # todo
    pm_ip, pm_port, agent_address = __get_pm_info("")
    del_host_url = "{}/del-host".format(agent_address)
    resp = req_util.req(RequestInfo.METHOD_DELETE,
                        del_host_url,
                        {'value': container_id})
    if resp.status_code == 200:
        msg = json.loads(resp.content)
        if msg['code'] == RequestInfo.SUCCESS_CODE.value:
            # stop success
            HostStatusRecord.objects.get(vm_id=container_id).delete()
            return JsonResponse({'status': 200, 'msg': 'stop success'})
        else:
            # stop failure
            return JsonResponse({'status': 500, 'msg': msg['msg']})
    else:
        return JsonResponse({'status': 500, 'msg': resp.content})


# TODO need design a table about pm and vm info
def __get_pm_info(vm_agent_info):
    # vm_id = vm_agent_info['']
    # vm_id = vm_agent_info['']
    # vm_ip = vm_agent_info['']
    pm_ip = "127.0.0.1"
    pm_port = "8000"

    return pm_ip, pm_port, "http://{}:{}".format(pm_ip, pm_port)


# get deploy host info
def get_deploy_host_func(request):
    online_hosts = HostStatusRecord.objects.exclude(status=DeployHostStatus.OFFLINE.value)
    instances = []
    for host in online_hosts:
        instance = {
            "id": host.vm_id,
            "ip": host.ip,
            "server_port": host.port,
            "status": host.status,
        }
        instances.append(instance)
    serialized_instances = json.dumps(instances)  # 将非字典对象序列化为 JSON 格式的字符串
    return JsonResponse(serialized_instances, safe=False)  # 设置


# receive init register info include host and vm
def register_info_collect(request):
    info = json.loads(request.body)
    """
    info: dict
        type: pm or vm
        vm_ip:
        pm_ip:
        pm_port:
        vm_name:
    """
    try:
        if info['type'] == HostType.VM.value:
            vm_ip = info['vm_ip']
            pm_ip = info['pm_ip']
            pm_port = info['pm_port']
            vm_name = info['vm_name']
        else:
            vm_ip = None
            pm_ip = info['pm_ip']
            pm_port = None
            vm_name = None

        host_register_info = HostRegisterInfo(host_type=info['type'],
                                              vm_ip=vm_ip,
                                              pm_ip=pm_ip)
        host_register_info.save()
        if info['type'] == HostType.VM.value:
            # TODO 这个地方是从 deploy host 里面查询的，就会导致查询最历史的数据
            query_set = (DeployHostRecord.objects
                         .filter(ip=vm_ip, pm_ip=pm_ip, pm_port=pm_port).order_by('-create_time'))
            query_set = list(query_set)
            vm_id = query_set[0].vm_id
            vm_port = query_set[0].port
            host_status_record = HostStatusRecord(vm_id=vm_id,
                                                  ip=vm_ip,
                                                  port=vm_port,
                                                  vm_name=vm_name,
                                                  status=DeployHostStatus.ONLINE.value,
                                                  pm_ip=pm_ip,
                                                  pm_port=pm_port)
            host_status_record.save()

        return JsonResponse({'status': 200,
                             'msg': "register success"})
    except Exception as e:
        return JsonResponse({'status': 500,
                             'msg': "register error, cause {}".format(str(e))})


# get vm id by pm use to scan local vm
def get_online_vm_id_by_pm(pm_ip, pm_port):
    vm_ids = (HostStatusRecord.objects
              .filter(status=DeployHostStatus.ONLINE.value)
              .filter(vm_id__in=DeployHostRecord.objects
                      .filter(pm_ip=pm_ip)
                      .values_list('vm_id', flat=True))
              .values_list('vm_id', flat=True))

    return JsonResponse({'status': 200, 'msg': "get success", 'data': vm_ids})


def sync_vm_info(request):
    infos = json.loads(request.body)
    """
    info: list
    id: vm id
    port: port
    
    select db and compare with id, add data if not exist
    """
    for info in infos:
        host_status_record = HostStatusRecord.objects.get(vm_id=info['id'])
        if not host_status_record:
            pass

    return JsonResponse({'status': 200,
                         'msg': 'sync success'})
