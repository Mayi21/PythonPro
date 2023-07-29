import getopt
import subprocess
import sys
import threading
import uuid

from kafka import KafkaConsumer
from kafka import KafkaProducer
from constant import KafkaInfo



res_consumer:KafkaConsumer = None
command_producer:KafkaProducer = None



def send_command(command):
    cmd_uuid = __get_uuid()
    command_producer.send(KafkaInfo.COMMAND_TOPIC.value,
                          key=cmd_uuid.encode("utf-8"),
                          value=command.encode("utf-8"))

# if use kafka, can't response immediately
# so this place can't use http method,just for not-timely job


def __handle_res():
    for msg in res_consumer:
        cmd_uuid = msg.key.decode()
        cmd_res = msg.value.decode()
        # todo persistence save




def __get_uuid():
    return str(uuid.uuid4())

def main(argv):
    bootstrap_servers = None
    try:
        opts, argvs = getopt.getopt(argv, "hs:", ["bootstrap_servers="])
    except getopt.GetoptError:
        print("agent.py -s <bootstrap_servers:port>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-s':
            bootstrap_servers = arg
            print(bootstrap_servers)
    if bootstrap_servers:
        global res_consumer
        global command_producer
        res_consumer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        command_producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    else:
        print("kafka config error")
        sys.exit(2)

    # handle msg as a thread task
    handle_msg_work = threading.Thread(target=__handle_res, name="handle_msg")
    handle_msg_work.start()


if __name__ == '__main__':
    main(sys.argv[1:])
