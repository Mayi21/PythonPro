#!/bin/bash

# 获取当前脚本所在目录的父目录
SCRIPT=$(dirname "$0")
PARENT_DIR=$(dirname "$(dirname "$SCRIPT")")

# 检查目录是否存在，如果不存在则创建
mkdir -p "${PARENT_DIR}/rpm_pkg/SOURCES"
mkdir -p "${PARENT_DIR}/rpm_pkg/SPECS"

# 复制 Python 脚本到 SOURCES 目录
cp -af "${PARENT_DIR}/agent/host_agent.py" "${PARENT_DIR}/rpm_pkg/SOURCES/"

# 打包脚本文件为 tar.gz 文件
tar czf "${PARENT_DIR}/rpm_pkg/SOURCES/host_agent-1.0.tar.gz" -C "${PARENT_DIR}/rpm_pkg/SOURCES" host_agent.py

# 构建 RPM 包
rpmbuild -v -bb --define "_topdir ${CUR_DIR}" ${CUR_DIR}/AgentClient.spec
