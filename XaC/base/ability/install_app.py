

'''
1.软件包名
2.位置（这个可以统一）
3.安装目录（可以为空，即默认安装在/opt下）
4.
'''
import logging
import os

from XaC.base.util.ssh_util import ssh_connect_and_execute


def install_jdk(software_pkg_name: str,software_pkg_path: str = '/home/pkg', dst_path: str = '/opt'):
    logging.info("start install jdk")
    cmd1 = 'tar -zxvf {} -C {}'.format(os.path.join(software_pkg_path, software_pkg_name), dst_path)
    # 配置连接参数
    host = "192.168.1.100"  # 替换为你的Linux主机IP
    user = "your_username"  # 替换为你的用户名
    pwd = "your_password"  # 替换为你的密码


    # 执行远程命令
    output, error = ssh_connect_and_execute(host, user, pwd, cmd1)