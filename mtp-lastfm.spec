#
Summary:	Last.Fm scrobbler for MTP devices
Name:		mtp-lastfm
Version:	0.83
Release:	4
License:	GPL v3
Group:		Applications
# http://github.com/woodenbrick/mtp-lastfm/tarball/%{version}
%define		commit 9a6ef66
Source0:	http://download.github.com/woodenbrick-%{name}-%{commit}.tar.gz
# Source0-md5:	0774bb8cf776e050dc627a2b0a8d7654
Patch0:		%{name}-desktop.patch
URL:		http://github.com/woodenbrick/mtp-lastfm
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:	python-devel
BuildRequires:	python-distutils-extra
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	libmtp-progs
Requires:	python-modules
Requires:	python-pygtk-glade
Requires:	python-pygtk-gtk
Requires:	sqlite3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The purpose of this program is to scrobble tracks from mtp devices
(such as the Creative Zen, or the Zune) to last.fm. You can love, ban
and tag tracks before scrobbling, and also use the ratings on your
device (5=Love, 1=Ban).

%prep
%setup -qn woodenbrick-%{name}-%{commit}
%patch0 -p1

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

# fix unsupported ??_?? locales
for dir in $RPM_BUILD_ROOT%{_localedir}/* ; do
	locale=`basename $dir`
	[ "$locale" = "zh_CN" ] && continue
	mv $RPM_BUILD_ROOT%{_localedir}/"$locale" $RPM_BUILD_ROOT%{_localedir}/"${locale%_*}"
done

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.textile CHANGELOG
%attr(755,root,root) %{_bindir}/*
%{_desktopdir}/*
%{_datadir}/%{name}
%{py_sitescriptdir}/mtplastfm
%{py_sitescriptdir}/*.egg-info
