以下是节点端收集程序的完整代码，基于之前的设计，包含系统信息收集、命令执行、脚本执行和文件上传功能，并通过 Flask 提供 RESTful API 接口：
### 功能说明

#### 1. 系统信息收集
- **API**: `GET /system_info`
- 返回CPU、内存、磁盘和平台信息的完整概要

#### 2. 命令执行
- **API**: `POST /execute_command`
- 请求体示例：
  ```json
  {"command": "ls"}
  ```
- 返回命令输出、错误信息和返回码

#### 3. 脚本执行
- **API**: `POST /execute_script`
- 请求体示例：
  ```json
  {"script_path": "/path/to/script.sh"}
  ```
- 返回脚本执行结果

#### 4. 文件上传
- **API**: `POST /upload_file`
- 请求体示例：
  ```json
  {
    "local_path": "/local/file.txt",
    "remote_path": "/remote/destination.txt",
    "hostname": "example.com",
    "username": "user",
    "password": "pass",
    "port": 22
  }
  ```
- 返回上传状态

#### 5. 健康检查
- **API**: `GET /health`
- 用于检查节点是否在线

---

### 依赖安装
运行前需要安装以下 Python 包：
```bash
pip install flask psutil paramiko
```

---

### 部署和使用

1. **部署**：
   - 将此文件保存为 `node_monitor.py`
   - 在每个节点上运行：`python node_monitor.py`
   - 确保防火墙允许访问端口 5000（或修改为其他端口）

2. **测试 API**：
   - 获取系统信息：
     ```bash
     curl http://node_ip:5000/system_info
     ```
   - 执行命令：
     ```bash
     curl -X POST -H "Content-Type: application/json" -d '{"command":"dir"}' http://node_ip:5000/execute_command
     ```
   - 执行脚本：
     ```bash
     curl -X POST -H "Content-Type: application/json" -d '{"script_path":"test.sh"}' http://node_ip:5000/execute_script
     ```
   - 上传文件：
     ```bash
     curl -X POST -H "Content-Type: application/json" -d '{"local_path":"file.txt","remote_path":"/tmp/file.txt","hostname":"example.com","username":"user","password":"pass"}' http://node_ip:5000/upload_file
     ```

---

### 注意事项
1. **安全性**：
   - 当前代码未实现认证，建议添加 API 密钥或 token 验证
   - 考虑使用 HTTPS 而不是 HTTP

2. **错误处理**：
   - 已包含基本错误处理，但可以根据需要增强日志记录

3. **性能**：
   - 对于高频请求，可添加缓存机制
   - 考虑使用异步框架（如 FastAPI）替代 Flask

4. **跨平台**：
   - 代码支持 Windows 和 Unix 系统，但某些命令需根据系统调整

这个完整代码可以直接部署在节点上，与 Web 端程序配合使用，提供监控和管理功能。