'''
负责接收命令和发送命令的执行结果
'''

import socket
from agent import run_command

SERVER_ADDRESS = '服务器IP地址'
SERVER_PORT = 12345  # 服务器端口号

def send_report(data):
    # 实现上报逻辑，将数据发送给服务器
    pass

def process_command(command):
    # 处理服务器发送的指令
    return run_command(command)


def start_agent():
    # 创建套接字并连接到服务器
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (SERVER_ADDRESS, SERVER_PORT)
    sock.connect(server_address)

    try:
        while True:
            # 接收服务器发送的数据
            data = sock.recv(1024).decode()
            if data:
                # 处理服务器发送的指令
                report_data = process_command(data)
                # 发送信息给服务器
                send_report(report_data)
    finally:
        # 关闭套接字连接
        sock.close()

# 启动Agent
if __name__ == "__main__":
    start_agent()
