Name:           agent-plugin
Version:        1.0.0
Release:        1%{?dist}
Summary:        A Python-based agent for collecting node information
License:        MIT
URL:            https://example.com/agent-plugin
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
Requires:       python3

%description
This package provides a Python-based agent plugin to collect system information
from nodes, such as CPU, memory, disk, and network usage. Dependencies are installed
via pip during the installation process.

%prep
%setup -q

%build
true

%install
# 创建安装目录
install -d %{buildroot}/usr/local/agent
install -d %{buildroot}/usr/local/agent/bin
install -d %{buildroot}/usr/local/agent/conf
install -d %{buildroot}/var/log/agent

# 安装 Python 源码
cp -r src/* %{buildroot}/usr/local/agent/
chmod 755 %{buildroot}/usr/local/agent/host_agent.py

# 安装配置文件
install -m 644 conf/agent.conf %{buildroot}/usr/local/agent/conf/

# 安装启动脚本
install -m 755 bin/agent-start.sh %{buildroot}/usr/local/agent/bin/agent-start

%post
# 安装 Python 依赖
/usr/bin/python3 -m ensurepip --upgrade
/usr/bin/python3 -m pip install --upgrade pip
/usr/bin/python3 -m pip install paramiko flask gunicorn requests uvicorn apscheduler fastapi psutil
echo "Agent plugin installed successfully. Run '/usr/local/agent/bin/agent-start' to begin collecting node info."

%files
/usr/local/agent/*
/usr/local/agent/bin/agent-start
/usr/local/agent/conf/agent.conf
%dir /var/log/agent

%changelog
* Tue Apr 08 2025 Your Name <your.email@example.com> - 1.0.0-1
- Initial release