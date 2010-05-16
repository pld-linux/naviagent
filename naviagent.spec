Summary:	Navisphere Agent and CLI
Summary(pl.UTF-8):	Agent i interfejs linii poleceń do Navisphere
Name:		naviagent
Version:	6.26.0.2.24
Release:	0.7
License:	EMC Corp
Group:		Applications/System
%if 0
Source0:	NAVIAGNTCLI_LINUX_V26.zip
# NoSource0-md5:	d94cec5596ee7aec1635de9140b27a89
NoSource:	0
%endif
Source1:	%{name}.init
URL:		https://powerlink.emc.com/
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	unzip
Requires(post,preun):	/sbin/chkconfig
# for 32bit libgcc
Requires:	libgcc_s.so.1
Requires:	rc-scripts >= 0.4.1.26
Obsoletes:	naviagentcli
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# avoid empty package
%define		_enable_debug_packages	0

%description
Navisphere Agent.

%description -l pl.UTF-8
Agent i interfejs linii poleceń do Navisphere.

%package -n navicli
Summary:	Navisphere CLI
Group:		Applications/System

%description -n navicli
Navisphere CLI.

%prep
%setup -qcT
%if 1
ln -s %{_sourcedir}/naviagentcli-6.26.0.2.24-0.3.i686.rpm naviagentcli.noarch.rpm
%endif

rpm2cpio naviagentcli.noarch.rpm | cpio -dimu

%if 1
mv usr/sbin bin
mv etc/Navisphere/* etc
%else
mv opt/Navisphere/bin .
mv opt/Navisphere/''etc .
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/etc/rc.d/init.d,/etc/Navisphere,/var/{log,run}/naviagent}
install -p bin/{naviagent,navicli,naviseccli} $RPM_BUILD_ROOT%{_sbindir}
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/naviagent
cp -a etc/SupportedFlareRevisions etc/agent.config $RPM_BUILD_ROOT%{_sysconfdir}/Navisphere

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add naviagent
%service naviagent restart

%preun
if [ "$1" = "0" ]; then
	%service -q naviagent stop
	/sbin/chkconfig --del naviagent
fi

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/Navisphere
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/Navisphere/SupportedFlareRevisions
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/Navisphere/agent.config
%attr(754,root,root) /etc/rc.d/init.d/naviagent
%attr(755,root,root) %{_sbindir}/naviagent
%dir %attr(750,root,root) /var/run/naviagent
%dir %attr(750,root,root) /var/log/naviagent

%files -n navicli
%attr(755,root,root) %{_sbindir}/navicli
%attr(755,root,root) %{_sbindir}/naviseccli
