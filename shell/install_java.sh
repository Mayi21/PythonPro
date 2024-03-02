#!/bin/bash

# 更新apt包索引
sudo apt update

# 安装OpenJDK 11
sudo apt install -y default-jdk

# 验证Java安装
java -version
