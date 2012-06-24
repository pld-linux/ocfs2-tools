Summary:	Tools for the OCFS2 filesystem
Summary(pl):	Narz�dzia dla systemu plik�w OCFS2
Name:		ocfs2-tools
Version:	1.1.2
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://oss.oracle.com/projects/ocfs2-tools/dist/files/source/v1.1/%{name}-%{version}.tar.gz
# Source0-md5:	f2412153cf33db29e10549c855c43e35
URL:		http://oss.oracle.com/projects/ocfs2-tools/
BuildRequires:	e2fsprogs-devel
BuildRequires:	glib2-devel
BuildRequires:	libcom_err-devel
BuildRequires:	libuuid-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	readline-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tools and support files for creating and managing OCFS2 volumes.

%description -l pl
Narz�dzia do tworzenia i zarz�dzania wolumenami OCFS2.

%package gtk
Summary:	GTK+ interface to OCFS2 Tools
Summary(pl):	Interfejs GTK+ do narz�dzi OCFS2
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	python-pygtk-gtk

%description gtk
GTK+ interface to OCFS2 Tools.

%description gtk -l pl
Interfejs GTK+ do narz�dzi OCFS2.

%prep
%setup -q

%build
%configure \
	--enable-dynamic-fsck=yes \
	--enable-dynamic-ctl=yes \
	--enable-ocfs2console=yes
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) /sbin/*
%{_mandir}/man8/*

%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%dir %{py_sitedir}/ocfs2interface
%attr(755,root,root) %{py_sitedir}/ocfs2interface/*.so
%{py_sitedir}/ocfs2interface/*.py[co]
