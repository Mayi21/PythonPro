Name:           agent-plugin
Version:        1.0.0
Release:        1%{?dist}
Summary:        A Python-based agent for collecting node information
License:        MIT
URL:            https://example.com/agent-plugin
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
Requires:       python3, python3-psutil

%description
This package provides a Python-based agent plugin to collect system information
from nodes, such as CPU, memory, disk, and network usage.

%prep
%setup -q

%build
true

%install
# 创建统一的安装目录
install -d %{buildroot}/usr/local/agent
install -d %{buildroot}/usr/local/agent/bin
install -d %{buildroot}/usr/local/agent/conf
install -d %{buildroot}/var/log/agent

# 安装 Python 源码到 /usr/local/agent/
cp -r src/* %{buildroot}/usr/local/agent/
chmod 755 %{buildroot}/usr/local/agent/agent.py

# 安装配置文件到 /usr/local/agent/conf/
install -m 644 conf/agent.conf %{buildroot}/usr/local/agent/conf/

# 安装启动脚本到 /usr/local/agent/bin/
install -m 755 bin/agent-start.sh %{buildroot}/usr/local/agent/bin/agent-start

%post
echo "Agent plugin installed successfully. Run '/usr/local/agent/bin/agent-start' to begin collecting node info."

%files
/usr/local/agent/*
/usr/local/agent/bin/agent-start
/usr/local/agent/conf/agent.conf
%dir /var/log/agent

%changelog
* Tue Apr 08 2025 Your Name <your.email@example.com> - 1.0.0-1
- Initial release