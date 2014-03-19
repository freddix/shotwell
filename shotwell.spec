Summary:	Photo organizer
Name:		shotwell
Version:	0.18.0
Release:	1
License:	LGPL
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/shotwell/0.18/%{name}-%{version}.tar.xz
# Source0-md5:	856b69fe67bc8bd42a6985e042041daf
Patch0:		%{name}-build.patch
URL:		http://www.yorba.org/shotwell/
BuildRequires:	dbus-glib-devel
BuildRequires:	gnome-doc-utils
BuildRequires:	gstreamer-plugins-base-devel
BuildRequires:	gtk+3-webkit-devel
BuildRequires:	json-glib-devel
BuildRequires:	libexif-devel
BuildRequires:	libgee-devel
BuildRequires:	libgexiv2-devel >= 0.10.0
BuildRequires:	libgphoto2-devel
BuildRequires:	libraw-devel
BuildRequires:	libsoup-devel
BuildRequires:	pkg-config
BuildRequires:	rest-devel
BuildRequires:	sqlite3-devel
BuildRequires:	udev-glib-devel
BuildRequires:	vala >= 0.16.0
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	hicolor-icon-theme
Requires:	glib-networking
Requires:	libgphoto2-runtime
Requires:	xdg-utils
Suggests:	gstreamer-plugins-bad
Suggests:	gstreamer-plugins-ugly
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/shotwell

%description
Photo organizer.

%prep
%setup -q
%patch0 -p1

%build
export CFLAGS="%{rpmcflags}"
./configure \
	--disable-desktop-update	\
	--disable-icon-update		\
	--disable-schemas-compile	\
	--lib=%{_lib}			\
	--libexec=%{_libexecdir}	\
	--prefix=%{_prefix}

%{__make} \
	CC="%{__cc}"				\
	LDFLAGS="%{rpmcflags} %{rpmldflags}"	\
	OPTFLAGS="%{rpmcflags}"			\
	USER_VALAFLAGS="-X -O2"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_iconsdir}/hicolor/scalable/apps}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_desktop_database_post
%update_gsettings_cache

%postun
%update_icon_cache hicolor
%update_desktop_database_postun
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_bindir}/shotwell
%attr(755,root,root) %{_libexecdir}/shotwell-settings-migrator
%attr(755,root,root) %{_libexecdir}/shotwell-video-thumbnailer

%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/plugins/builtin
%attr(755,root,root) %{_libdir}/%{name}/plugins/builtin/*.so
%{_libdir}/%{name}/plugins/builtin/*.glade
%{_libdir}/%{name}/plugins/builtin/*.png

%{_datadir}/%{name}
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/shotwell.*

%{_datadir}/glib-2.0/schemas/org.yorba.shotwell-extras.gschema.xml
%{_datadir}/glib-2.0/schemas/org.yorba.shotwell.gschema.xml

