#!/bin/bash

# 检查必要的环境变量是否设置
if [[ -z "$MYSQL_URL" || -z "$MYSQL_USER" || -z "$MYSQL_PASSWD" || -z "$DRIVER_URL" ]]; then
  echo "Error: MySQL environment variables not set."
  exit 1
fi

# 编辑 hive-site.xml 文件
cat > /usr/local/hive/conf/hive-site.xml <<EOF
<configuration>
  <!-- 使用外部 MySQL 数据库作为元数据存储 -->
  <property>
    <name>javax.jdo.option.ConnectionURL</name>
    <value>${MYSQL_URL}</value>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionDriverName</name>
    <value>${DRIVER_URL}</value>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionUserName</name>
    <value>${MYSQL_USER}</value>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionPassword</name>
    <value>${MYSQL_PASSWD}</value>
  </property>

  <!-- 其他配置参数 -->
  <property>
    <name>hive.server2.authentication</name>
    <value>CUSTOM</value>
  </property>

  <property>
    <name>hive.server2.custom.authentication.class</name>
    <value>org.apache.hive.service.auth.PasswdAuthenticationProvider</value>
  </property>
  <property>
    <name>hive.server2.transport.mode</name>
    <value>binary</value>
  </property>

  <property>
    <name>hive.server2.thrift.http.port</name>
    <value>10001</value> <!-- 或者其他你选择的端口号 -->
  </property>
  <property>
    <name>hive.server2.thrift.bind.host</name>
    <value>0.0.0.0</value>
  </property>
</configuration>
EOF
echo "hadoop:123456" >> /usr/local/hive/conf/passwd
