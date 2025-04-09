#!/bin/bash
WORK_DIR=/usr/local/agent

# 启动服务
start_service() {
    echo "Starting my_service..."
    python3 ${WORK_DIR}/host_agent.py
}

# 停止服务
stop_service() {
    echo "Stopping my_service..."
    # 这里是停止服务的命令，替换为你的实际停止命令
    # 例如：/path/to/my_service stop
}

# 检查服务状态
check_service_status() {
    # 检查服务的状态，使用curl命令检查服务是否响应
    if curl -sSf "http://127.0.0.1:5000/v1/health" > /dev/null; then
        echo "my_service is running."
    else
        echo "my_service is not running."
    fi
}

install_service() {
    pip install -r ${WORK_DIR}/requirements.txt
}

# 根据输入参数执行相应操作
if [ "$1" = "start" ]; then
    start_service
elif [ "$1" = "stop" ]; then
    stop_service
elif [ "$1" = "check_status" ]; then
    check_service_status
elif [ "$1" = "install" ]; then
    install_service
else
    echo "Usage: $0 {start|stop|check_status}"
    exit 1
fi
