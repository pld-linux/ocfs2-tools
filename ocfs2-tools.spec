#
# Conditional build:
%bcond_with	cman		# cman support
%bcond_without	corosync	# Corosync support
%bcond_without	dlm		# DLM support
%bcond_with	openais		# OpenAIS ckpt support
%bcond_without	pacemaker	# Pacemaker support
%bcond_without	gtk2		# GTK+ 2 ocfs2console tool
#
Summary:	Tools for the OCFS2 filesystem
Summary(pl.UTF-8):	Narzędzia dla systemu plików OCFS2
Name:		ocfs2-tools
Version:	1.8.6
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	https://github.com/markfasheh/ocfs2-tools/archive/%{name}-%{version}.tar.gz
# Source0-md5:	fc64af70a6a2533948f47fa9cb2fc1c4
Source1:	ocfs2.init
Source2:	o2cb.init
Source3:	o2cb.sysconfig
Patch0:		%{name}-tinfo.patch
Patch2:		%{name}-linux.patch
Patch3:		%{name}-format.patch
Patch4:		%{name}-link.patch
URL:		http://oss.oracle.com/projects/ocfs2-tools/
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake
%{?with_cman:BuildRequires:	cman-devel}
%{?with_corosync:BuildRequires:	corosync-devel}
BuildRequires:	device-mapper-devel
%{?with_dlm:BuildRequires:	dlm-devel}
BuildRequires:	e2fsprogs-devel
BuildRequires:	glib2-devel >= 2.2.3
BuildRequires:	libblkid-devel >= 1.36
BuildRequires:	libcom_err-devel
BuildRequires:	libuuid-devel
BuildRequires:	ncurses-devel
%{?with_openais:BuildRequires:	openais-devel}
%{?with_pacemaker:BuildRequires:	pacemaker-devel}
BuildRequires:	pkgconfig
%{?with_gtk2:BuildRequires:	python-devel >= 1:2.3}
%{?with_gtk2:BuildRequires:	python-pygtk-gtk}
BuildRequires:	readline-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires:	glib2 >= 2.2.3
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tools and support files for creating and managing OCFS2 volumes.

%description -l pl.UTF-8
Narzędzia do tworzenia i zarządzania wolumenami OCFS2.

%package devel
Summary:	Header files and develpment documentation for ocfs2-tools
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumetacja do ocfs2-tools
Group:		Development/Libraries

%description devel
Header files and develpment documentation for ocfs2-tools.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumetacja do ocfs2-tools.

%package gtk
Summary:	GTK+ interface to OCFS2 Tools
Summary(pl.UTF-8):	Interfejs GTK+ do narzędzi OCFS2
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	python-pygtk-gtk

%description gtk
GTK+ interface to OCFS2 Tools.

%description gtk -l pl.UTF-8
Interfejs GTK+ do narzędzi OCFS2.

%prep
%setup -q -n %{name}-%{name}-%{version}
%patch0 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

sed -i -e 's#-Wno-format##g' */Makefile

%build
%{__aclocal} -I .
%{__autoconf}

%configure \
	%{!?with_corosync:ac_cv_header_corosync_cpg_h=no ac_cv_header_openais_cpg_h=no} \
	%{!?with_cman:ac_cv_lib_cman_cman_replyto_shutdown=no} \
	%{!?with_dlm:ac_cv_lib_dlmcontrol_dlmc_fs_connect=no} \
	%{!?with_openais:ac_cv_header_openais_saCkpt_h=no} \
	%{!?with_pacemaker:ac_cv_lib_crmcluster_crm_get_peer=no} \
	--enable-dynamic-fsck=yes \
	--enable-dynamic-ctl=yes \
	%{?with_gtk2:--enable-ocfs2console=yes}

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D documentation/samples/cluster.conf $RPM_BUILD_ROOT%{_sysconfdir}/ocfs2/cluster.conf
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ocfs2
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/o2cb
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/o2cb
install -d $RPM_BUILD_ROOT/dlm

%if %{with gtk2}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/ocfs2interface/*.py
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/chkconfig --add o2cb
/sbin/chkconfig --add ocfs2
%service o2cb restart
%service ocfs2 restart

%preun
if [ "$1" = "0" ]; then
	%service -q ocfs2 stop
	%service -q o2cb stop
	/sbin/chkconfig --del ocfs2
	/sbin/chkconfig --del o2cb
fi

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS MAINTAINERS README README.O2CB documentation/*.txt
%attr(754,root,root) /etc/rc.d/init.d/o2cb
%attr(754,root,root) /etc/rc.d/init.d/ocfs2
%attr(755,root,root) /sbin/debugfs.ocfs2
%attr(755,root,root) /sbin/defragfs.ocfs2
%attr(755,root,root) /sbin/fsck.ocfs2
%attr(755,root,root) /sbin/mkfs.ocfs2
%attr(755,root,root) /sbin/mounted.ocfs2
%attr(755,root,root) /sbin/mount.ocfs2
%attr(755,root,root) /sbin/o2cb
%attr(755,root,root) /sbin/o2cb_ctl
%attr(755,root,root) /sbin/o2cluster
%attr(755,root,root) /sbin/o2image
%attr(755,root,root) /sbin/ocfs2_hb_ctl
%attr(755,root,root) /sbin/tunefs.ocfs2
%if %{with corosync} && %{with openais} && %{with dlm}
%if %{with cman}
%attr(755,root,root) /sbin/ocfs2_controld.cman
%endif
%if %{with pacemaker}
%attr(755,root,root) /sbin/ocfs2_controld.pcmk
%endif
%endif
%attr(755,root,root) %{_bindir}/o2info
%attr(755,root,root) %{_sbindir}/o2hbmonitor
%dir %{_sysconfdir}/ocfs2
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ocfs2/cluster.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/o2cb
%dir /dlm
%{_mandir}/man1/o2info.1*
%{_mandir}/man5/o2cb.sysconfig.5.*
%{_mandir}/man5/ocfs2.cluster.conf.5.*
%{_mandir}/man7/o2cb.7*
%{_mandir}/man7/ocfs2.7.*
%{_mandir}/man8/debugfs.ocfs2.8*
%{_mandir}/man8/defragfs.ocfs2.8.*
%{_mandir}/man8/fsck.ocfs2.8*
%{_mandir}/man8/fsck.ocfs2.checks.8*
%{_mandir}/man8/mkfs.ocfs2.8*
%{_mandir}/man8/mounted.ocfs2.8*
%{_mandir}/man8/mount.ocfs2.8*
%{_mandir}/man8/o2cb.8.*
%{_mandir}/man8/o2cb_ctl.8*
%{_mandir}/man8/o2cluster.8.*
%{_mandir}/man8/o2hbmonitor.8.*
%{_mandir}/man8/o2image.8*
%{_mandir}/man8/ocfs2_hb_ctl.8*
%{_mandir}/man8/tunefs.ocfs2.8*

%files devel
%defattr(644,root,root,755)
%{_includedir}/o2cb
%{_includedir}/o2dlm
%{_includedir}/ocfs2
%{_includedir}/ocfs2-kernel
%{_libdir}/libo2cb.a
%{_libdir}/libo2dlm.a
%{_libdir}/libocfs2.a
%{_pkgconfigdir}/o2cb.pc
%{_pkgconfigdir}/o2dlm.pc
%{_pkgconfigdir}/ocfs2.pc

%if %{with gtk2}
%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ocfs2console
%dir %{py_sitedir}/ocfs2interface
%attr(755,root,root) %{py_sitedir}/ocfs2interface/gidlemodule.so
%attr(755,root,root) %{py_sitedir}/ocfs2interface/o2cbmodule.so
%attr(755,root,root) %{py_sitedir}/ocfs2interface/ocfs2module.so
%attr(755,root,root) %{py_sitedir}/ocfs2interface/plistmodule.so
%{py_sitedir}/ocfs2interface/*.py[co]
%{_mandir}/man8/ocfs2console.8*
%endif
