#!/bin/bash

# 设置JDK安装路径
JDK_INSTALL_DIR="/usr/local/jdk"
# 设置Hadoop安装路径
HADOOP_INSTALL_DIR="/usr/local/hadoop"
# 设置Hive安装路径
HIVE_INSTALL_DIR="/usr/local/hive"

# 创建安装目录
sudo mkdir -p $JDK_INSTALL_DIR
sudo mkdir -p $HADOOP_INSTALL_DIR
sudo mkdir -p $HIVE_INSTALL_DIR

# 下载JDK，Hadoop和Hive的安装包（这里以官网地址为例）
# 注意：您可能需要根据您的系统架构和版本选择合适的安装包下载链接
JDK_URL="https://download.oracle.com/java/17/latest/jdk-17_linux-x64_bin.tar.gz"
HADOOP_URL="https://downloads.apache.org/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz"
HIVE_URL="https://downloads.apache.org/hive/hive-3.1.2/apache-hive-3.1.2-bin.tar.gz"

# 下载并解压安装包
sudo wget -P $JDK_INSTALL_DIR $JDK_URL
sudo tar -xzvf $JDK_INSTALL_DIR/jdk-*.tar.gz -C $JDK_INSTALL_DIR --strip-components=1
sudo wget -P $HADOOP_INSTALL_DIR $HADOOP_URL
sudo tar -xzvf $HADOOP_INSTALL_DIR/hadoop-*.tar.gz -C $HADOOP_INSTALL_DIR --strip-components=1
sudo wget -P $HIVE_INSTALL_DIR $HIVE_URL
sudo tar -xzvf $HIVE_INSTALL_DIR/apache-hive-*.tar.gz -C $HIVE_INSTALL_DIR --strip-components=1

# 配置环境变量
echo "export JAVA_HOME=$JDK_INSTALL_DIR" >> ~/.bashrc
echo "export HADOOP_HOME=$HADOOP_INSTALL_DIR" >> ~/.bashrc
echo "export HIVE_HOME=$HIVE_INSTALL_DIR" >> ~/.bashrc
echo "export PATH=\$JAVA_HOME/bin:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin:\$HIVE_HOME/bin:\$PATH" >> ~/.bashrc
source ~/.bashrc

# 复制Hadoop配置文件模板，并修改配置
cp $HADOOP_INSTALL_DIR/etc/hadoop/*.xml $HADOOP_INSTALL_DIR/etc/hadoop/*.sh $HADOOP_INSTALL_DIR/etc/hadoop/*.cmd $HADOOP_INSTALL_DIR/etc/hadoop/*.template $HADOOP_INSTALL_DIR/etc/hadoop/*-env.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-policy.xml $HADOOP_INSTALL_DIR/etc/hadoop/*-config.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-regex.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-default.xml $HADOOP_INSTALL_DIR/etc/hadoop/*-site.xml $HADOOP_INSTALL_DIR/etc/hadoop/*-hosts $HADOOP_INSTALL_DIR/etc/hadoop/*-keys.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-users $HADOOP_INSTALL_DIR/etc/hadoop/*-groups $HADOOP_INSTALL_DIR/etc/hadoop/*-files.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-tmp.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $HADOOP_INSTALL_DIR/etc/hadoop/*-groups.sh $
