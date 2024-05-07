Name: host_agent
Version: 1.0
Release: 1%{?dist}
Summary: Description of your package

License: YourLicense
URL: http://www.example.com
Source0: %{name}-%{version}.tar.gz

BuildArch: noarch

%description
Your description here

%prep
%setup -q

%build
# Nothing needed here for a Python script

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
cp -a %{_builddir}/%{name}-%{version}/* $RPM_BUILD_ROOT/usr/bin/

%files
/usr/bin/host_agent.py

%changelog
