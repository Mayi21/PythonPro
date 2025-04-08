from kazoo.client import KazooClient

# 创建一个客户端，设置连接到的 ZooKeeper 服务器
zk = KazooClient(hosts='192.168.100.132:2181')

# 开始连接
zk.start()


try:
    data, stat = zk.get("/hbase/meta-region-server")
    try:
        # Try decoding as utf-8
        text = data.decode('utf-8')
        print("Version: %s, data: %s" % (stat.version, text))
    except UnicodeDecodeError:
        # Handle data as binary if it fails to decode
        print("Data could not be decoded as UTF-8, handled as binary data.")
        print("Version: %s, data length: %d bytes" % (stat.version, len(data)))
except Exception as e:
    print("An error occurred: %s" % str(e))

