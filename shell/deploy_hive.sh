#!/bin/bash

# 更新apt包索引
sudo apt update

# 启动MySQL服务
sudo service mysql start

# 下载Hive压缩包
wget https://downloads.apache.org/hive/hive-3.1.2/apache-hive-3.1.2-bin.tar.gz

# 解压Hive压缩包
tar -xvf apache-hive-3.1.2-bin.tar.gz

# 将Hive文件夹移动到/opt目录下
sudo mv apache-hive-3.1.2-bin /opt/hive

# 设置Hive环境变量
echo "export HIVE_HOME=/opt/hive" >> ~/.bashrc
echo "export PATH=\$PATH:\$HIVE_HOME/bin" >> ~/.bashrc
source ~/.bashrc

# 配置Hive元数据库连接到外部MySQL数据库
cp $HIVE_HOME/conf/hive-default.xml.template $HIVE_HOME/conf/hive-site.xml
echo "<configuration>" >> $HIVE_HOME/conf/hive-site.xml
echo "  <property>" >> $HIVE_HOME/conf/hive-site.xml
echo "    <name>javax.jdo.option.ConnectionURL</name>" >> $HIVE_HOME/conf/hive-site.xml
echo "    <value>jdbc:mysql://external_mysql_host:3306/metastore?createDatabaseIfNotExist=true</value>" >> $HIVE_HOME/conf/hive-site.xml
echo "    <description>JDBC connect string for a JDBC metastore</description>" >> $HIVE_HOME/conf/hive-site.xml
echo "  </property>" >> $HIVE_HOME/conf/hive-site.xml
echo "  <property>" >> $HIVE_HOME/conf/hive-site.xml
echo "    <name>javax.jdo.option.ConnectionDriverName</name>" >> $HIVE_HOME/conf/hive-site.xml
echo "    <value>com.mysql.jdbc.Driver</value>" >> $HIVE_HOME/conf/hive-site.xml
echo "    <description>Driver class name for a JDBC metastore</description>" >> $HIVE_HOME/conf/hive-site.xml
echo "  </property>" >> $HIVE_HOME/conf/hive-site.xml
echo "  <property>" >> $HIVE_HOME/conf/hive-site.xml
echo "    <name>javax.jdo.option.ConnectionUserName</name>" >> $HIVE_HOME/conf/hive-site.xml
echo "    <value>your_mysql_username</value>" >> $HIVE_HOME/conf/hive-site.xml
echo "    <description>Username to use against metastore database</description>" >> $HIVE_HOME/conf/hive-site.xml
echo "  </property>" >> $HIVE_HOME/conf/hive-site.xml
echo "  <property>" >> $HIVE_HOME/conf/hive-site.xml
echo "    <name>javax.jdo.option.ConnectionPassword</name>" >> $HIVE_HOME/conf/hive-site.xml
echo "    <value>your_mysql_password</value>" >> $HIVE_HOME/conf/hive-site.xml
echo "    <description>password to use against metastore database</description>" >> $HIVE_HOME/conf/hive-site.xml
echo "  </property>" >> $HIVE_HOME/conf/hive-site.xml
echo "</configuration>" >> $HIVE_HOME/conf/hive-site.xml

# 初始化Hive元数据库
schematool -dbType mysql -initSchema

# 配置Hive监听端口
echo "hive.server2.enable=true" >> $HIVE_HOME/conf/hive-site.xml
echo "hive.server2.authentication=PAM" >> $HIVE_HOME/conf/hive-site.xml
echo "hive.server2.authentication.pam.services=login" >> $HIVE_HOME/conf/hive-site.xml
echo "hive.server2.enable.doAs=false" >> $HIVE_HOME/conf/hive-site.xml

# 启动Hive服务
nohup $HIVE_HOME/bin/hive --service metastore &> /opt/logs/hive/metastore.log &
nohup $HIVE_HOME/bin/hive --service hiveserver2 &> /opt/logs/hive/hiveserver2.log &

# 验证Hive安装
hive --version
