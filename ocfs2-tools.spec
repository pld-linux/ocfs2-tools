#
# Conditional build:
%bcond_without gtk2	# build without GTK
#
Summary:	Tools for the OCFS2 filesystem
Summary(pl.UTF-8):	Narzędzia dla systemu plików OCFS2
Name:		ocfs2-tools
Version:	1.4.4
Release:	5
License:	GPL v2
Group:		Applications/System
Source0:	http://oss.oracle.com/projects/ocfs2-tools/dist/files/source/v1.4/%{name}-%{version}.tar.gz
# Source0-md5:	f7ae245e8baa499aa56d7af25a7885d5
Source1:	ocfs2.init
Source2:	o2cb.init
Source3:	o2cb.sysconfig
Patch0:		%{name}-tinfo.patch
Patch1:		%{name}-vla-initializer.patch
URL:		http://oss.oracle.com/projects/ocfs2-tools/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cman-devel
BuildRequires:	device-mapper-devel
BuildRequires:	e2fsprogs-devel
BuildRequires:	glib2-devel >= 2.2.3
BuildRequires:	libuuid-devel
BuildRequires:	ncurses-devel
BuildRequires:	openais-devel
BuildRequires:	pkgconfig
%{?with_gtk2:BuildRequires:	python-devel}
%{?with_gtk2:BuildRequires:	python-pygtk-gtk}
BuildRequires:	readline-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.268
#BuildRequires:	scons
Requires(post):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		filterout_ld	-Wl,--as-needed

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
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__aclocal} -I .
%{__autoconf}

%configure \
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
rm $RPM_BUILD_ROOT%{py_sitedir}/ocfs2interface/*.py
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
%doc documentation/*.txt
%attr(754,root,root) /etc/rc.d/init.d/o2cb
%attr(754,root,root) /etc/rc.d/init.d/ocfs2
%attr(755,root,root) /sbin/*
%dir %{_sysconfdir}/ocfs2
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ocfs2/cluster.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/o2cb
%dir /dlm
%{_mandir}/man[78]/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_libdir}/lib*.a
%{_pkgconfigdir}/*.pc

%if %{with gtk2}
%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%dir %{py_sitedir}/ocfs2interface
%attr(755,root,root) %{py_sitedir}/ocfs2interface/*.so
%{py_sitedir}/ocfs2interface/*.py[co]
%endif
