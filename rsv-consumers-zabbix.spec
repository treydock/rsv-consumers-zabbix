Name:      rsv-consumers-zabbix
Version:   3.7.10
Release:   1%{?dist}
Summary:   RSV Consumer for Zabbix

Group:     Applications/Monitoring
License:   Apache 2.0
URL:       https://twiki.grid.iu.edu/bin/view/MonitoringInformation/RSV

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


%pre
# Create the rsv user/group
getent group rsv >/dev/null || groupadd -r rsv
getent passwd rsv >/dev/null || useradd -r -g rsv -d /var/rsv -s /bin/sh -c "RSV monitoring" rsv


%prep
%setup -q


%install
rm -fr $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_libexecdir}/rsv/consumers/zabbix-consumer
%config %{_sysconfdir}/rsv/meta/consumers/zabbix-consumer.meta
%config(noreplace) %{_sysconfdir}/rsv/consumers/zabbix-consumer.conf
%config(noreplace) %{_sysconfdir}/rsv/rsv-zabbix.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/rsv-consumers-zabbix
%attr(-,rsv,rsv) %{_localstatedir}/log/rsv/consumers

%changelog
* Mon Dec 16 2013  <treydock@tamu.edu> - 3.7.10-1
- Creating a first RPM for rsv-consumers-zabbix
