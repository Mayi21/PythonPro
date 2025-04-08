# 包的基本信息
Name:           agent-plugin
Version:        1.0.0
Release:        1%{?dist}
Summary:        A Python-based agent for collecting node information
License:        MIT
URL:            https://example.com/agent-plugin
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
Requires:       python3, python3-psutil, python3-pyyaml

%description
This package provides a Python-based agent plugin to collect system information
from nodes, such as CPU, memory, disk, and network usage. It is designed to be
installed via RPM and run as a service.

%prep
%setup -q

%build
# Python 项目通常无需编译，直接打包即可
# 如果需要构建，可以在这里调用 python3 setup.py build
true

%install
# 创建目标目录
install -d %{buildroot}/usr/lib/agent
install -d %{buildroot}/etc/agent
install -d %{buildroot}/usr/bin
install -d %{buildroot}/var/log/agent

# 安装 Python 源码
cp -r src/* %{buildroot}/usr/lib/agent/
chmod 755 %{buildroot}/usr/lib/agent/main.py

# 安装配置文件
install -m 644 conf/agent.conf %{buildroot}/etc/agent/

# 安装启动脚本
install -m 755 bin/agent-start.sh %{buildroot}/usr/bin/agent-start

%post
# 安装后的操作，例如打印提示信息
echo "Agent plugin installed successfully. Run 'agent-start' to begin collecting node info."
echo "Configuration file is located at /etc/agent/agent.conf"

%preun
# 卸载前的操作（可选）
echo "Stopping agent if running..."

%postun
# 卸载后的操作（可选）
echo "Agent plugin uninstalled."

%files
/usr/lib/agent/*
/etc/agent/agent.conf
/usr/bin/agent-start
%dir /var/log/agent

%changelog
* Tue Apr 08 2025 Your Name <your.email@example.com> - 1.0.0-1
- Initial release of agent-plugin