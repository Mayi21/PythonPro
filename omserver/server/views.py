# dashboard/views.py
import json
import time

from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

from .models import AgentInfo

NODES = [
    {'name': 'Node1', 'url': 'http://node1_ip:5000'},
    {'name': 'Node2', 'url': 'http://node2_ip:5000'},
]

@api_view(['GET'])
def node_list(request):
    return Response(NODES)

@api_view(['GET'])
def node_detail(request, node_name):
    node = next((n for n in NODES if n['name'] == node_name), None)
    if not node:
        return Response({'error': 'Node not found'}, status=404)
    try:
        response = requests.get(f"{node['url']}/system_info", timeout=5)
        return Response(response.json())
    except requests.RequestException as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def execute_command(request, node_name):
    node = next((n for n in NODES if n['name'] == node_name), None)
    if not node:
        return Response({'error': 'Node not found'}, status=404)
    command = request.data.get('command')
    if not command:
        return Response({'error': 'No command provided'}, status=400)
    try:
        response = requests.post(f"{node['url']}/execute_command", json={'command': command}, timeout=10)
        return Response(response.json())
    except requests.RequestException as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def upload_file(request, node_name):
    node = next((n for n in NODES if n['name'] == node_name), None)
    if not node:
        return Response({'error': 'Node not found'}, status=404)
    data = request.data
    required_fields = ['local_path', 'remote_path', 'hostname', 'username', 'password']
    if not all(field in data for field in required_fields):
        return Response({'error': 'Missing required fields'}, status=400)
    try:
        response = requests.post(f"{node['url']}/upload_file", json=data, timeout=10)
        return Response(response.json())
    except requests.RequestException as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def update_vm_info(request):
    data = json.loads(request.body)
    if 'node_ip' not in data:
        return Response({'error': 'Missing required fields'}, status=400)
    if 'node_sn' not in data:
        return Response({'error': 'Missing required fields'}, status=400)
    node_ip = data['node_ip']
    node_sn = data['node_sn']
    agent_info = AgentInfo(ip=node_ip, sn=node_sn, )
    agent_info.save()
    return Response({'status': 'OK'})

@api_view(['POST'])
def deploy_vm(request):
    '''
    下发虚拟机

    '''
    data = json.loads(request.body)

