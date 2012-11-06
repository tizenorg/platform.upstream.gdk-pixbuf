%define gdk_pixbuf_binary_version 2.10.0

Name:           gdk-pixbuf
Version:        2.26.4
Release:        2.3
Summary:        An image loading library
License:        LGPL-2.1+
Group:          System/Libraries
Source:         http://download.gnome.org/sources/gdk-pixbuf/2.26/%{name}-%{version}.tar.xz
Source1:        macros.gdk-pixbuf
Source98:       baselibs.conf
BuildRequires:  gettext-tools
BuildRequires:  libjasper-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  pkgconfig(glib-2.0) >= 2.31.0
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(x11)

%description
gdk-pixbuf is an image loading library that can be extended by loadable
modules for new image formats. It is used by toolkits such as GTK+ or
Clutter.

Summary:        An image loading library
Group:          System/Libraries
Requires(post): gdk-pixbuf-query-loaders
Recommends:     %{name}-lang = %{version}

%package -n typelib-GdkPixbuf
Summary:        An image loading library -- Introspection bindings
Group:          System/Libraries

%description -n typelib-GdkPixbuf
gdk-pixbuf is an image loading library that can be extended by loadable
modules for new image formats. It is used by toolkits such as GTK+ or
Clutter.

This package provides the GObject Introspection bindings for gdk-pixbuf.

%package query-loaders
Summary:        An image loading library - Utility to create loaders cache
Group:          System/Libraries

%description query-loaders
gdk-pixbuf is an image loading library that can be extended by loadable
modules for new image formats. It is used by toolkits such as GTK+ or
Clutter.

This package contains the utility to create the cache file needed for
loadable modules.

%package devel
Summary:        An image loading library - Development Files
Group:          Development/Languages/C and C++
Requires:       gdk-pixbuf = %{version}
Requires:       typelib-GdkPixbuf = %{version}

%description devel
gdk-pixbuf is an image loading library that can be extended by loadable
modules for new image formats. It is used by toolkits such as GTK+ or
Clutter.

This package contains development files for gdk-pixbuf.

%prep
%setup -q

%build
%configure \
        --disable-static \
        --enable-introspection \
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

# Convenient %define for the scriplets
%if "%_lib" == "lib64"
%define _gdk_pixbuf_query_loaders %{_bindir}/gdk-pixbuf-query-loaders-64
%else
%define _gdk_pixbuf_query_loaders %{_bindir}/gdk-pixbuf-query-loaders
%endif
%define _gdk_pixbuf_query_loaders_update_cache %{_gdk_pixbuf_query_loaders} --update-cache

%lang_package

%post -n gdk-pixbuf
/sbin/ldconfig
%if 0
# In case gdk-pixbuf gets installed before gdk-pixbuf-query-loaders,
# we don't want to fail. So we make the call to gdk-pixbuf-query-loaders
# dependent on the existence of the binary. This is why we also have a %post
# for gdk-pixbuf-query-loaders.
%endif
if test -f %{_gdk_pixbuf_query_loaders}; then
  %{_gdk_pixbuf_query_loaders_update_cache}
fi

%post query-loaders
%if 0
# If we install gdk-pixbuf-query-loaders for the first time, then we should run
# it in case gdk-pixbuf was installed first (ie, if
# %{_libdir}/gdk-pixbuf-2.0/%{gdk_pixbuf_binary_version} already exists) which
# means gdk-pixbuf-query-loaders couldn't run there.
%endif
if [ $1 == 1 ]; then
  test -d %{_libdir}/gdk-pixbuf-2.0/%{gdk_pixbuf_binary_version}
  if test $? -eq 0; then
    %{_gdk_pixbuf_query_loaders_update_cache}
  fi
fi

%if 0
# No need to call gdk-pixbuf-query-loaders in postun:
# - if it's an upgrade, it will have been called in post
# - if it's an uninstall, we don't care about this anymore
%endif

%postun -n gdk-pixbuf -p /sbin/ldconfig

%files -n gdk-pixbuf
%defattr(-, root, root)
%doc AUTHORS COPYING NEWS README
%{_libdir}/libgdk_pixbuf-2.0.so.0*
%{_libdir}/libgdk_pixbuf_xlib-2.0.so.0*
%dir %{_libdir}/gdk-pixbuf-2.0
%dir %{_libdir}/gdk-pixbuf-2.0/%{gdk_pixbuf_binary_version}
%dir %{_libdir}/gdk-pixbuf-2.0/%{gdk_pixbuf_binary_version}/loaders
%{_libdir}/gdk-pixbuf-2.0/%{gdk_pixbuf_binary_version}/loaders/*.so
%ghost %{_libdir}/gdk-pixbuf-2.0/%{gdk_pixbuf_binary_version}/loaders.cache

%files -n typelib-GdkPixbuf
%defattr(-,root,root)
%{_libdir}/girepository-1.0/GdkPixbuf-2.0.typelib

%files query-loaders
%defattr(-, root, root)
%{_bindir}/gdk-pixbuf-query-loaders*
%{_mandir}/man1/gdk-pixbuf-query-loaders*.1*

%files devel
%defattr(-, root, root)
%{_bindir}/gdk-pixbuf-csource
%{_bindir}/gdk-pixbuf-pixdata
%{_mandir}/man1/gdk-pixbuf-csource.1*
%{_includedir}/gdk-pixbuf-2.0
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_datadir}/gir-1.0/GdkPixbuf-2.0.gir
%doc %{_datadir}/gtk-doc/html/gdk-pixbuf
%{_sysconfdir}/rpm/macros.gdk-pixbuf
