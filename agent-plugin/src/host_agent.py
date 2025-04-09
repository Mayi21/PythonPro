# node_monitor.py
import psutil
import platform
from flask import Flask, jsonify, request
import subprocess
import os
import paramiko
from datetime import datetime

app = Flask(__name__)


class SystemMonitor:
    def __init__(self):
        self.system_info = {}

    def get_cpu_info(self):
        """获取CPU信息"""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        self.system_info['cpu'] = {
            'usage_percent': cpu_percent,
            'cores': cpu_count,
            'logical_cores': psutil.cpu_count(logical=True)
        }
        return self.system_info['cpu']

    def get_memory_info(self):
        """获取内存信息"""
        memory = psutil.virtual_memory()
        self.system_info['memory'] = {
            'total': f"{memory.total / (1024 ** 3):.2f} GB",
            'available': f"{memory.available / (1024 ** 3):.2f} GB",
            'percent': memory.percent
        }
        return self.system_info['memory']

    def get_disk_info(self):
        """获取磁盘信息"""
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'total': f"{usage.total / (1024 ** 3):.2f} GB",
                    'used': f"{usage.used / (1024 ** 3):.2f} GB",
                    'free': f"{usage.free / (1024 ** 3):.2f} GB",
                    'percent': usage.percent
                })
            except:
                continue
        self.system_info['disk'] = disks
        return self.system_info['disk']

    def execute_command(self, command):
        """执行系统命令（兼容Python 3.4+）"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,  # 捕获标准输出
                stderr=subprocess.PIPE,  # 捕获标准错误
                universal_newlines=True  # 返回字符串而不是字节，兼容3.4+
            )
            return {
                'output': result.stdout,
                'error': result.stderr,
                'return_code': result.returncode
            }
        except Exception as e:
            return {'error': str(e)}

    def execute_shell_script(self, script_path):
        """执行shell脚本（兼容Python 3.4+）"""
        if not os.path.exists(script_path):
            return {'error': 'Script file not found'}

        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ['cmd.exe', '/c', script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
            else:
                result = subprocess.run(
                    ['bash', script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
            return {
                'output': result.stdout,
                'error': result.stderr,
                'return_code': result.returncode
            }
        except Exception as e:
            return {'error': str(e)}

    def upload_file(self, local_path, remote_path, hostname, username, password, port=22):
        """上传文件到远程服务器"""
        if not os.path.exists(local_path):
            return {'error': 'Local file not found'}

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, port, username, password)
            sftp = ssh.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            ssh.close()
            return {'status': 'success', 'message': f'File uploaded to {remote_path}'}
        except Exception as e:
            return {'error': str(e)}

    def get_system_summary(self):
        """获取系统信息概要"""
        self.get_cpu_info()
        self.get_memory_info()
        self.get_disk_info()
        self.system_info['platform'] = {
            'system': platform.system(),
            'node': platform.node(),
            'release': platform.release(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return self.system_info


# 创建监控实例
monitor = SystemMonitor()


# API 路由
@app.route('/system_info', methods=['GET'])
def get_system_info():
    """获取系统信息API"""
    return jsonify(monitor.get_system_summary())


@app.route('/execute_command', methods=['POST'])
def execute_command():
    """执行命令API"""
    data = request.get_json()
    if not data or 'command' not in data:
        return jsonify({'error': 'No command provided'}), 400
    result = monitor.execute_command(data['command'])
    return jsonify(result)


@app.route('/execute_script', methods=['POST'])
def execute_script():
    """执行脚本API"""
    data = request.get_json()
    if not data or 'script_path' not in data:
        return jsonify({'error': 'No script path provided'}), 400
    result = monitor.execute_shell_script(data['script_path'])
    return jsonify(result)


@app.route('/upload_file', methods=['POST'])
def upload_file():
    """上传文件API"""
    data = request.get_json()
    required_fields = ['local_path', 'remote_path', 'hostname', 'username', 'password']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    result = monitor.upload_file(
        local_path=data['local_path'],
        remote_path=data['remote_path'],
        hostname=data['hostname'],
        username=data['username'],
        password=data['password'],
        port=data.get('port', 22)
    )
    return jsonify(result)


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查API"""
    return jsonify({'status': 'healthy', 'node': platform.node()})


if __name__ == "__main__":
    # 在节点上运行，监听特定端口
    app.run(host='0.0.0.0', port=5000, debug=True)