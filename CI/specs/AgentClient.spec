Name:           mypackage
Version:        1.0
Release:        1
Summary:        My sample package
License:        GPLv3

%description
agent rpm package.

# 定义rpm文件安装后，这个文件要放在那里
%define _prefix /usr/local/agent

# 把要打包的文件移入到构建目录下面
%install
mkdir -p $RPM_BUILD_ROOT%{_prefix}/plugin
cp -pR %{_pro_dir}/* $RPM_BUILD_ROOT%{_prefix}/plugin/


# 定义文件属性和这个rpm包里面包含哪些文件
%files
%defattr(-,root,root)
%{_prefix}/plugin/*
