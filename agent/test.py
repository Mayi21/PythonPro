import getopt
import json
import subprocess
import sys
import uuid

import requests

from constant import *
from utils import __exec_cmd


def main(argv):
    bootstrap_servers = None
    try:
        opts, argvs = getopt.getopt(argv, "hs:", ["bootstrap_servers="])
    except getopt.GetoptError:
        print("test.py -s <bootstrap_servers:port>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-s':
            bootstrap_servers = arg
    print(bootstrap_servers)


def test_upload_file():
    files = {'file': open('temp/test1.jpeg', 'rb')}
    resp = requests.post('http://127.0.0.1:8000/uploadfiles', files=files)
    if resp.status_code == 200:
        print("upload successful")
    else:
        print("failed to upload")


def deploy_host(port: str):
    out = __exec_cmd('docker run -d -p {}:8000 --name agent_{} agent'.format(port, port))
    if len(out['result']) != 64:
        print(out['result'])
    print(out['result'])


def stop_host(container_id: str):
    out = __exec_cmd('docker stop {}'.format(container_id))
    if len(out['result']) != 64:
        return {'error': out['result']}
    return {'success': out['result']}
    pass


def del_host(container_id: str):
    out = __exec_cmd('docker container rm {}'.format(container_id))
    if len(out['result']) != 64:
        return {'error': out['result']}
    return {'success': out['result']}


def sync_vm_info():
    out = __exec_cmd(DockerCMD.GET_RUNNING_VM.value)['result']
    out = out.split("\n")
    if len(out) == 1:
        return
    vm_infos = []
    for info in out[1:]:
        id = info[:12]
        out = __exec_cmd("{} {}".format(DockerCMD.GET_VM_PORT.value,
                                        id))['result']
        port = out.split("->")[-1].split(":")[-1]
        vm_infos.append({'id': id,
                         'port': port})

    return vm_infos


if __name__ == "__main__":
    # print(deploy_host('8081'))
    #  print(del_host('d2aafd335ca9ea87c73e3e467efa03a26a5dd9fba65a30e49fa32079a5b65ae9'))
    # print(stop_host('a4d5ddc33b320c7571043679fb3eba6cc9b6b91165549d7ddbe8dd867330acc4'))

    # print(DockerCMD.DEL_VM.value)
    # print('200'== RespCode.SUCCESS_CODE.value)
    print(sync_vm_info())
