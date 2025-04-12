# 初始化centos7的脚本
## 更换repo源
cp -a /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak
curl -kv https://mirrors.huaweicloud.com/repository/conf/CentOS-7-anon.repo > /etc/yum.repos.d/CentOS-Base.repo
yum clean all
yum makecache
yum -y install epel-release net-tools lsof vim wget python3

## 关闭防火墙
systemctl stop firewalld
systemctl disable firewalld