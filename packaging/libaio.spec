Name:           libaio
Version:        0.3.109
Release:        0
Summary:        Linux-Native Asynchronous I/O Access Library
License:        LGPL-2.1+
Group:          Development/Libraries
Url:            http://kernel.org/pub/linux/libs/aio/
Source:         libaio-%{version}.tar.bz2
Source2:        baselibs.conf

%description
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has
a richer API and capability set than the simple POSIX async I/O
facility. This library provides the Linux-native API for async I/O. The
POSIX async I/O facility requires this library to provide
kernel-accelerated async I/O capabilities, as do applications that
require the Linux-native async I/O API.


%package devel
Summary:        Development Files for Linux-native Asynchronous I/O Access
Group:          Development/Libraries/C and C++
Requires:       %name = %version, glibc-devel

%description devel
This package provides header files to include, and libraries to link
with, for the Linux-native asynchronous I/O facility ("async I/O", or
"aio").



%prep
%setup -q

%build
make %{?_smp_mflags} CC="%__cc" OPTFLAGS="$RPM_OPT_FLAGS"

%install
make install prefix=%{buildroot}/usr libdir=%{buildroot}/%{_lib}
%if "%_lib" == "lib64"
mv "%buildroot/usr/lib" "%buildroot/usr/lib64"
%endif
rm -f "%buildroot/%_libdir"/*.a
# Strip dumb /usr/src/... off
t=$(readlink -f "%buildroot/%_lib/libaio.so.1")
ln -fs "${t##*/}" "%buildroot/%_lib/libaio.so.1"
t=$(readlink -f "%buildroot/%_libdir/libaio.so")
ln -fs "${t#%buildroot}" "%buildroot/%_libdir/libaio.so"

%post  -p /sbin/ldconfig

%postun  -p /sbin/ldconfig

%files 
%defattr(644,root,root,755)
%license COPYING
%attr(0755,root,root) /%{_lib}/libaio.*

%files devel
%defattr(644,root,root,755)
/usr/include/libaio.h
%_libdir/libaio.so

%changelog
