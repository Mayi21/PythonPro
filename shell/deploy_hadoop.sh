#!/bin/bash

# 更新apt包索引
sudo apt update

# 下载Hadoop压缩包
wget https://downloads.apache.org/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz

# 解压Hadoop压缩包
tar -xvf hadoop-3.3.1.tar.gz

# 将Hadoop文件夹移动到/opt目录下
sudo mv hadoop-3.3.1 /opt/hadoop

# 设置Hadoop环境变量
echo "export HADOOP_HOME=/opt/hadoop" >> ~/.bashrc
echo "export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin" >> ~/.bashrc
source ~/.bashrc

# 配置Hadoop环境
cp $HADOOP_HOME/etc/hadoop/*.xml $HADOOP_HOME/etc/hadoop/*.cmd /opt/hadoop/etc/hadoop
sudo sed -i '/^export JAVA_HOME/ s:.*:export JAVA_HOME=/usr/lib/jvm/default-java\nexport HADOOP_HOME=/opt/hadoop\nexport HADOOP_INSTALL=$HADOOP_HOME\nexport HADOOP_MAPRED_HOME=$HADOOP_HOME\nexport HADOOP_COMMON_HOME=$HADOOP_HOME\nexport HADOOP_HDFS_HOME=$HADOOP_HOME\nexport YARN_HOME=$HADOOP_HOME\nexport HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native\nexport PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin\nexport HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"': /opt/hadoop/etc/hadoop/hadoop-env.sh

# 格式化HDFS
hdfs namenode -format

# 启动Hadoop
start-dfs.sh
start-yarn.sh

# 验证Hadoop安装
hadoop version
