import time

from kafka import KafkaProducer, KafkaAdminClient

# Kafka 服务器地址
bootstrap_servers = '192.168.100.132:9092'
# 要写入的主题
topic = 'text-input-topic'

# 创建 KafkaProducer 实例
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
messages = ["tomato potato carrot tomato lettuce potato carrot tomato lettuce tomato"]
# messages = ["apple banana grape apple orange banana grape apple orange apple"]
# messages = ["cat dog bird cat fish dog bird cat fish cat"]
# messages = ["rose lily tulip rose daisy lily tulip rose daisy rose"]
# messages = ["car bike bus car train bike bus car train car"]
messages = ["table chair sofa table lamp chair sofa table lamp table"]
# messages = ["bread cheese milk bread butter cheese milk bread butter bread"]
# messages = ["sparrow pigeon eagle sparrow crow pigeon eagle sparrow crow"]
# messages = ["fish crab shrimp fish lobster crab shrimp fish lobster fish"]
messages = ["shirt pants dress shirt coat pants dress shirt coat shirt"]





try:
    # 创建 KafkaAdminClient 实例
    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

    # 循环发送消息
    for msg in messages:
        # 发送消息到主题
        producer.send(topic, value=msg.encode('utf-8'))
        print(f'Sent: {msg}')
        time.sleep(5)

    # 等待所有消息发送完成
    producer.flush()
finally:
    # 关闭 KafkaProducer
    producer.close()
