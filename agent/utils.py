import json

import subprocess

import requests

from constant import RequestInfo


# execute shell command
def __exec_cmd(cmd):
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        result = output.decode().strip() if output else error.decode().strip()
        return {"result": result}
    except Exception as e:
        return {"result": str(e)}


def check_shell_file(file_name):
    pass

class LogUtil:
    pass



class HttpUtil:

    def __post(self, url, data, headers):
        resp = requests.post(url=url,
                             data=data,
                             headers=headers)
        return resp

    def __get(self, url, data, params, headers):
        resp = requests.get(url=url,
                            data=data,
                            params=params,
                            headers=headers)
        return resp

    def __put(self, url, data, params, headers):
        resp = requests.put(url=url,
                            data=data,
                            params=params,
                            headers=headers)
        return resp

    def __delete(self, url, data, params, headers):
        resp = requests.delete(url=url,
                               params=params,
                               data=data,
                               headers=headers)
        return resp

    def req(self, method: str, url: str, data, params, headers=RequestInfo.REQ_HEADERS.value):
        data = json.dumps(data)
        if method == RequestInfo.METHOD_GET.value:
            return self.__get(url=url, data=data, params=params, headers=headers)
        elif method == RequestInfo.METHOD_PUT.value:
            return self.__put(url=url, data=data, params=params, headers=headers)
        elif method == RequestInfo.METHOD_POST.value:
            return self.__post(url=url, data=data, headers=headers)
        else:
            return self.__delete(url=url, data=data, params=params, headers=headers)


if __name__ == '__main__':
    print(get_config())
