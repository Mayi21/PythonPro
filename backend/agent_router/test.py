import getopt
import sys
import uuid

import requests


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

if __name__ == "__main__":
   test_upload_file()