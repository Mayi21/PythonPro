#!/bin/bash

# 设置Hadoop安装路径
HADOOP_INSTALL_DIR="/usr/local/hadoop"

# 创建安装目录
 mkdir -p $HADOOP_INSTALL_DIR

# 下载Hadoop安装包（这里以官网地址为例）
HADOOP_DOWNLOAD_URL="https://archive.apache.org/dist/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz"
wget -P $HADOOP_INSTALL_DIR $HADOOP_DOWNLOAD_URL

# 解压安装包
 tar -xzvf $HADOOP_INSTALL_DIR/hadoop-*.tar.gz -C $HADOOP_INSTALL_DIR --strip-components=1

# 配置Hadoop环境变量
echo "export HADOOP_HOME=$HADOOP_INSTALL_DIR" >> ~/.bashrc
echo 'export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin' >> ~/.bashrc
source ~/.bashrc

# 配置Hadoop伪分布式模式
cp $HADOOP_INSTALL_DIR/etc/hadoop/mapred-site.xml.template $HADOOP_INSTALL_DIR/etc/hadoop/mapred-site.xml
echo "<configuration><property><name>mapreduce.framework.name</name><value>yarn</value></property></configuration>" >> $HADOOP_INSTALL_DIR/etc/hadoop/mapred-site.xml

# 配置Hadoop单节点模式
cp $HADOOP_INSTALL_DIR/etc/hadoop/core-site.xml.template $HADOOP_INSTALL_DIR/etc/hadoop/core-site.xml
echo "<configuration><property><name>fs.defaultFS</name><value>hdfs://localhost:9000</value></property></configuration>" >> $HADOOP_INSTALL_DIR/etc/hadoop/core-site.xml
cp $HADOOP_INSTALL_DIR/etc/hadoop/hdfs-site.xml.template $HADOOP_INSTALL_DIR/etc/hadoop/hdfs-site.xml
echo "<configuration><property><name>dfs.replication</name><value>1</value></property></configuration>" >> $HADOOP_INSTALL_DIR/etc/hadoop/hdfs-site.xml

# 格式化HDFS
hdfs namenode -format

# 启动Hadoop集群
start-dfs.sh
start-yarn.sh

# 验证Hadoop安装
hadoop version
