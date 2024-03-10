#!/bin/bash

# 设置JDK安装路径
JDK_INSTALL_DIR="/usr/local/jdk"

# 创建安装目录
 mkdir -p $JDK_INSTALL_DIR

# 下载JDK安装包（这里以官网地址为例）
JDK_DOWNLOAD_URL="https://download.oracle.com/java/17/latest/jdk-17_linux-x64_bin.tar.gz"
wget -P $JDK_INSTALL_DIR $JDK_DOWNLOAD_URL

# 解压安装包
 tar -xzvf $JDK_INSTALL_DIR/jdk-*.tar.gz -C $JDK_INSTALL_DIR --strip-components=1

# 配置环境变量
echo "export JAVA_HOME=$JDK_INSTALL_DIR" >> ~/.bashrc
echo "export PATH=\$JAVA_HOME/bin:\$PATH" >> ~/.bashrc
source ~/.bashrc

# 验证安装
java -version
