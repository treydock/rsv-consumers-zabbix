Name:      rsv-consumers-zabbix
Version:   0.1.0
Release:   1%{?dist}
Summary:   RSV Consumer for Zabbix

Group:     Applications/System
License:   Apache 2.0
URL:       https://github.com/treydock/rsv-consumers-zabbix

Source0:   %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires: gratia-probe-metric
Requires: rsv-consumers

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
Requires: python-simplejson
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%description
%{summary}

%prep
%setup -q

%build

%install
rm -fr $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README.md zabbix_template.xml
%{_libexecdir}/rsv/consumers/zabbix-consumer
%config %{_sysconfdir}/rsv/meta/consumers/zabbix-consumer.meta
%config(noreplace) %{_sysconfdir}/rsv/consumers/zabbix-consumer.conf
%config(noreplace) %{_sysconfdir}/rsv/rsv-zabbix.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/rsv-consumers-zabbix
%attr(-,rsv,rsv) %{_localstatedir}/log/rsv/consumers

%changelog
* Tue Nov 11 2014  <treydock@tamu.edu> - 0.1.0-1
- Update build to version 0.1.0

* Mon Dec 16 2013  <treydock@tamu.edu> - 0.0.1-1
- Creating a first RPM for rsv-consumers-zabbix
