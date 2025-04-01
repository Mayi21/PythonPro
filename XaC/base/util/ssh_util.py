import paramiko
import time


def ssh_connect_and_execute(hostname, username, password, command, port=22):
    """
    远程登录Linux节点并执行命令

    参数:
    hostname: 目标主机IP或域名
    username: SSH用户名
    password: SSH密码
    command: 要执行的命令
    port: SSH端口，默认22
    """
    try:
        # 创建SSH客户端对象
        ssh_client = paramiko.SSHClient()

        # 自动添加主机密钥
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # 连接远程主机
        print(f"正在连接 {hostname}...")
        ssh_client.connect(hostname=hostname,
                           username=username,
                           password=password,
                           port=port)
        print("连接成功！")

        # 执行命令
        print(f"正在执行命令: {command}")
        stdin, stdout, stderr = ssh_client.exec_command(command)

        # 等待命令执行完成
        time.sleep(1)

        # 获取命令输出
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        # 打印结果
        if output:
            print("命令输出：")
            print(output)
        if error:
            print("错误输出：")
            print(error)

        return output, error

    except Exception as e:
        print(f"发生错误: {str(e)}")
        return None, str(e)

    finally:
        # 关闭连接
        ssh_client.close()
        print("SSH连接已关闭")


# 使用示例
if __name__ == "__main__":
    # 配置连接参数
    host = "192.168.1.100"  # 替换为你的Linux主机IP
    user = "your_username"  # 替换为你的用户名
    pwd = "your_password"  # 替换为你的密码
    cmd = "ls -l"  # 要执行的命令，例如：查看系统信息"uname -a"

    # 执行远程命令
    output, error = ssh_connect_and_execute(host, user, pwd, cmd)