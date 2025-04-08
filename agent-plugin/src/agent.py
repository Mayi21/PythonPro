import getopt
import subprocess
import sys

from kafka import KafkaConsumer
from kafka import KafkaProducer
from constant import KafkaInfo

res_producer: KafkaProducer = None
command_consumer: KafkaProducer = None


def __runcommand(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    print(output)
    return output.decode()


def receive_command():
    for msg in command_consumer:
        cmd_uuid = msg.key.decode()
        cmd = msg.value.decode()
        try:
            res = __runcommand(cmd)
            __send_res(cmd_uuid, res)
        except Exception as e:
            print(e)


def __send_res(cmd_uuid, res):
    res_producer.send(KafkaInfo.RES_TOPIC.value, key=cmd_uuid.encode('utf-8'),
                      value=res.encode('utf-8'))


def main(argv):
    bootstrap_servers = None
    try:
        opts, argvs = getopt.getopt(argv, "hs:", ["bootstrap_servers="])
    except getopt.GetoptError:
        print("agent-plugin.py -s <bootstrap_servers:port>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-s':
            bootstrap_servers = arg
            print(bootstrap_servers)
    if bootstrap_servers:
        global res_producer
        global command_consumer
        res_producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        command_consumer = KafkaConsumer(KafkaInfo.COMMAND_TOPIC.value, bootstrap_servers=bootstrap_servers)
    else:
        print("kafka config error")
        sys.exit(2)
    receive_command()


if __name__ == '__main__':
    main(sys.argv[1:])
