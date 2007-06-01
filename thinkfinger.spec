%define lib_major 0
%define lib_name %mklibname %name %{lib_major}

Name: thinkfinger
Summary: Driver for the SGS Thomson Microelectronics fingerprint reader found in most IBM/Lenovo ThinkPads
Version: 0.3
Release: %mkrel 2
License: GPL
Group: System/Kernel and hardware
Source: http://ovh.dl.sourceforge.net/sourceforge/thinkfinger/%{name}-%{version}.tar.bz2
URL: http://thinkfinger.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-build

BuildRequires: pam-devel
BuildRequires: libusb-devel

%description
ThinkFinger is a driver for the SGS Thomson Microelectronics 
fingerprint reader found in most IBM/Lenovo ThinkPads.

%files
%defattr(-,root,root)
%{_sbindir}/tf-tool
%_mandir/man1/tf-tool.1.bz2
%_mandir/man8/pam_thinkfinger.8.bz2

#--------------------------------------------------------------------

%package -n %{lib_name}
Summary:  %{summary}
Group: %{group}

%description -n %{lib_name}
%post -n %{lib_name}
/sbin/ldconfig
%postun -n %{lib_name}
/sbin/ldconfig

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/libthinkfinger.so.0.0.0
%{_libdir}/libthinkfinger.so.0
%{_libdir}/security/pam_thinkfinger.so
#--------------------------------------------------------------------

%package -n %{lib_name}-devel
Summary:  %{summary}
Group: %{group}
Provides: %name-devel
Requires: %{lib_name} = %{version}

%description -n %{lib_name}-devel

%files -n %{lib_name}-devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/libthinkfinger.pc
%{_libdir}/libthinkfinger.la
%{_libdir}/libthinkfinger.so
%{_includedir}/libthinkfinger.h
#--------------------------------------------------------------------

%prep
%setup -q

%build
export CFLAGS="$RPM_OPT_FLAGS"

%configure2_5x \
    --enable-static=no 

%make

%install
make DESTDIR=%buildroot install

%clean
rm -rf %buildroot 
