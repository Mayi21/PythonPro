import os
import threading
import time
import uuid

from kafka import KafkaProducer
from kafka import KafkaConsumer

from utils import get_uuid
from time import sleep

# bootstrap_servers = os.getenv("kafka_bootstrap_servers")
bootstrap_servers = "localhost:9092"
command_topic = "server_command"
res_topic = "client_res"
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)


def server_send_command(command):
    command_uuid = __get_command_uuid()
    producer.send(command_topic, key=command_uuid.encode("utf-8"), value=command.encode('utf-8'))


def server_receive_res():
    consumer = KafkaConsumer(command_topic, bootstrap_servers=bootstrap_servers)
    for c in consumer:
        print(c.key.decode())
        print(c.value.decode())


def __get_command_uuid():
    return get_uuid()


command_res_thread = threading.Thread(target=server_receive_res, name="command_consumer")
command_res_thread.start()

start_index = 0
while True:
    server_send_command(str(start_index))
    start_index += 1
    time.sleep(2)
