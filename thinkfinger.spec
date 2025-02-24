%define lib_major 0
%define lib_name %mklibname %name %{lib_major}
%define lib_devel_name %mklibname %name -d

Name: thinkfinger
Summary: Driver and tools for the fingerprint reader found in most IBM/Lenovo ThinkPads
Version: 0.3
Release: %mkrel 7
License: GPLv2+
Group: System/Kernel and hardware
Source: http://ovh.dl.sourceforge.net/sourceforge/thinkfinger/%{name}-%{version}.tar.bz2
Patch: thinkfinger-0.3-format-strings.patch
URL: https://thinkfinger.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-build
Requires: kmod(uinput)
BuildRequires: pam-devel
BuildRequires: libusb-devel
BuildRequires: doxygen

%description
ThinkFinger is a driver for the SGS Thomson Microelectronics 
fingerprint reader found in most IBM/Lenovo ThinkPads.

This package contains the tool to acquire and verify fingerprints, and the
PAM module for authentication with fingerprints.

%files
%defattr(-,root,root)
%doc README NEWS COPYING AUTHORS INSTALL
%{_sbindir}/tf-tool
%_mandir/man1/tf-tool.*
%attr(700,root,root) %dir %{_sysconfdir}/pam_thinkfinger
/%_lib/security/pam_thinkfinger.so
%_mandir/man8/pam_thinkfinger.8.*

#--------------------------------------------------------------------

%package -n %{lib_name}
Summary:  %{summary}
Group: %{group}

%description -n %{lib_name}
ThinkFinger is a driver for the SGS Thomson Microelectronics 
fingerprint reader found in most IBM/Lenovo ThinkPads.

This package contains the driver library.

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/libthinkfinger.so.%{lib_major}*

#--------------------------------------------------------------------

%package -n %{lib_devel_name}
Summary:  %{summary}
Group: %{group}
# for new devel library policy
Obsoletes: %mklibname %name 0 -d
Provides: %name-devel = %version-%release
Requires: %{lib_name} = %{version}

%description -n %{lib_devel_name}
ThinkFinger is a driver for the SGS Thomson Microelectronics 
fingerprint reader found in most IBM/Lenovo ThinkPads.

This package contains the development files and documentation for
thinkfinger.

%files -n %{lib_devel_name}
%defattr(-,root,root)
%doc docs/autodocs/html
%{_libdir}/pkgconfig/libthinkfinger.pc
%{_libdir}/libthinkfinger.la
%{_libdir}/libthinkfinger.so
%{_includedir}/libthinkfinger.h

#--------------------------------------------------------------------


%prep
%setup -q
%patch -p1

%build
export CFLAGS="$RPM_OPT_FLAGS"

%configure2_5x \
    --enable-static=no \
    --with-securedir=/%_lib/security

%make

%install
rm -rf %buildroot
%makeinstall_std
mkdir -m 700 -p %buildroot/%_sysconfdir/pam_thinkfinger

%clean
rm -rf %buildroot 
