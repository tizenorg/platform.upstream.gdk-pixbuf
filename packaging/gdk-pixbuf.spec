%define gdk_pixbuf_binary_version 2.10.0
%bcond_with introspection
Name:           gdk-pixbuf
Version:        2.28.1
Release:        0
Summary:        An image loading library
License:        LGPL-2.1+
Group:          Multimedia/Image Library
Source:         http://download.gnome.org/sources/gdk-pixbuf/2.27/%{name}-%{version}.tar.xz
Source1:        macros.gdk-pixbuf
Source98:       baselibs.conf
Source1001: 	gdk-pixbuf.manifest
BuildRequires:  gettext-tools
Url:            http://developer.gnome.org/
BuildRequires:  libjasper-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  pkgconfig(glib-2.0) >= 2.31.0
%if %{with introspection}
BuildRequires:  pkgconfig(gobject-introspection-1.0)
%endif
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(x11)
Requires(post): gdk-pixbuf-query-loaders

%description
gdk-pixbuf is an image loading library that can be extended by loadable
modules for new image formats. It is used by toolkits such as GTK+ or
Clutter.

%package -n typelib-GdkPixbuf
Summary:        An image loading library -- Introspection bindings
Group:          Multimedia/Image Library

%description -n typelib-GdkPixbuf
gdk-pixbuf is an image loading library that can be extended by loadable
modules for new image formats. It is used by toolkits such as GTK+ or
Clutter.

This package provides the GObject Introspection bindings for gdk-pixbuf.

%package query-loaders
Summary:        An image loading library - Utility to create loaders cache
Group:          Multimedia/Image Library

%description query-loaders
gdk-pixbuf is an image loading library that can be extended by loadable
modules for new image formats. It is used by toolkits such as GTK+ or
Clutter.

This package contains the utility to create the cache file needed for
loadable modules.

%package devel
Summary:        An image loading library - Development Files
Group:          Development/Libraries
Requires:       gdk-pixbuf = %{version}
%if %{with introspection}
Requires:       typelib-GdkPixbuf = %{version}
%endif

%description devel
gdk-pixbuf is an image loading library that can be extended by loadable
modules for new image formats. It is used by toolkits such as GTK+ or
Clutter.

This package contains development files for gdk-pixbuf.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS=`echo $RPM_OPT_FLAGS |sed -e 's/atom/i686/g'`
%configure \
        --disable-static \
%if %{with introspection}
        --enable-introspection \
%endif
        --with-libjasper \
        --with-x11
%{__make} %{?_smp_mflags}

%install
%make_install
%find_lang %{name}
touch %{buildroot}%{_libdir}/gdk-pixbuf-2.0/%{gdk_pixbuf_binary_version}/loaders.cache
%if "%_lib" == "lib64"
  mv %{buildroot}%{_bindir}/gdk-pixbuf-query-loaders %{buildroot}%{_bindir}/gdk-pixbuf-query-loaders-64
  mv %{buildroot}%{_mandir}/man1/gdk-pixbuf-query-loaders.1 %{buildroot}%{_mandir}/man1/gdk-pixbuf-query-loaders-64.1
%endif
# Install rpm macros
mkdir -p %{buildroot}%{_sysconfdir}/rpm
cp %{S:1} %{buildroot}%{_sysconfdir}/rpm

###########################################################################
# Note: when updating scriptlets, don't forget to also update baselibs.conf
###########################################################################

# Convenient define for the scriplets
%if "%_lib" == "lib64"
%define _gdk_pixbuf_query_loaders %{_bindir}/gdk-pixbuf-query-loaders-64
%else
%define _gdk_pixbuf_query_loaders %{_bindir}/gdk-pixbuf-query-loaders
%endif
%define _gdk_pixbuf_query_loaders_update_cache %{_gdk_pixbuf_query_loaders} --update-cache

%lang_package

%post -n gdk-pixbuf
/sbin/ldconfig
if test -f %{_gdk_pixbuf_query_loaders}; then
  %{_gdk_pixbuf_query_loaders_update_cache}
fi

%post query-loaders
if [ $1 == 1 ]; then
  test -d %{_libdir}/gdk-pixbuf-2.0/%{gdk_pixbuf_binary_version}
  if test $? -eq 0; then
    %{_gdk_pixbuf_query_loaders_update_cache}
  fi
fi

%postun -n gdk-pixbuf -p /sbin/ldconfig

%files -n gdk-pixbuf
%manifest %{name}.manifest
%defattr(-, root, root)
%license COPYING
%{_libdir}/libgdk_pixbuf-2.0.so.0*
%{_libdir}/libgdk_pixbuf_xlib-2.0.so.0*
%dir %{_libdir}/gdk-pixbuf-2.0
%dir %{_libdir}/gdk-pixbuf-2.0/%{gdk_pixbuf_binary_version}
%dir %{_libdir}/gdk-pixbuf-2.0/%{gdk_pixbuf_binary_version}/loaders
%{_libdir}/gdk-pixbuf-2.0/%{gdk_pixbuf_binary_version}/loaders/*.so
%ghost %{_libdir}/gdk-pixbuf-2.0/%{gdk_pixbuf_binary_version}/loaders.cache

%if %{with introspection}
%files -n typelib-GdkPixbuf
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/girepository-1.0/GdkPixbuf-2.0.typelib
%endif

%files query-loaders
%manifest %{name}.manifest
%defattr(-, root, root)
%{_bindir}/gdk-pixbuf-query-loaders*
%{_mandir}/man1/gdk-pixbuf-query-loaders*.1*

%files devel
%manifest %{name}.manifest
%defattr(-, root, root)
%{_bindir}/gdk-pixbuf-csource
%{_bindir}/gdk-pixbuf-pixdata
%{_mandir}/man1/gdk-pixbuf-csource.1*
%{_includedir}/gdk-pixbuf-2.0
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%if %{with introspection}
%{_datadir}/gir-1.0/GdkPixbuf-2.0.gir
%endif
%doc %{_datadir}/gtk-doc/html/gdk-pixbuf
%{_sysconfdir}/rpm/macros.gdk-pixbuf
