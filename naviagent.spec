Summary:	Navisphere Agent and CLI
Name:		naviagentcli
Version:	6.26.0.2.24
Release:	0.2
License:	EMC Corp
Group:		Applications/System
Source0:	NAVIAGNTCLI_LINUX_V26.zip
# NoSource0-md5:	d94cec5596ee7aec1635de9140b27a89
NoSource:	0
URL:		https://powerlink.emc.com/
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Navisphere Agent and CLI

%prep
%setup -qc
rpm2cpio naviagentcli.noarch.rpm | cpio -dimu

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/etc/rc.d/init.d,/etc/Navisphere}

install opt/Navisphere/bin/{naviagent,navicli,naviseccli} $RPM_BUILD_ROOT%{_sbindir}
install etc/init.d/naviagent $RPM_BUILD_ROOT/etc/rc.d/init.d
cp -a etc/Navisphere/SupportedFlareRevisions etc/Navisphere/agent.config $RPM_BUILD_ROOT%{_sysconfdir}/Navisphere

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/Navisphere
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/Navisphere/SupportedFlareRevisions
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/Navisphere/agent.config
%attr(754,root,root) /etc/rc.d/init.d/naviagent
%attr(755,root,root) %{_sbindir}/naviagent
%attr(755,root,root) %{_sbindir}/navicli
%attr(755,root,root) %{_sbindir}/naviseccli