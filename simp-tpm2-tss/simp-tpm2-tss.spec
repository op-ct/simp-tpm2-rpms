# Adapted from
#
Name:           simp-tpm2-tss
Version:        1.3.0
Release:        4%{?dist}
Summary:        TPM2.0 Software Stack

# SIMP customization:
%define _prefix /usr/local

# The entire source code is under BSD except implementation.h and tpmb.h which
# is under TCGL(Trusted Computing Group License).
#
# UPDATE: The entirety of the source code is actually BSD.  The TCGL was
# attributed in error in the upstream sources, and was removed in a subsequent
# patch:
#
#    https://github.com/tpm2-software/tpm2-tss/commit/f3cd7fe5ee796227177d4828f0245a72ed03fb64
#
License:        BSD
URL:            https://github.com/tpm2-software/tpm2-tss
#Source0:        https://github.com/tpm2-software/tpm2-tss/releases/download/%{version}/%{name}-%{version}.tar.gz
Source0:        %{version}/%{name}-%{version}.tar.gz
Source1:        60-tpm-udev.rules

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  autoconf-archive
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  systemd

%description
NOTE: This software has been repackaged for use with EL7 for SIMP 6.2.X

tpm2-tss is a software stack supporting Trusted Platform Module(TPM) 2.0 system
APIs. It sits between TPM driver and applications, providing TPM2.0 specified
APIs for applications to access TPM module through kernel TPM drivers.

%prep
%autosetup -n %{name}-%{version}

%build
PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{_libdir}/pkgconfig ./bootstrap
PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{_libdir}/pkgconfig %configure --disable-static --disable-silent-rules
%make_build

%install
%make_install
find %{buildroot}%{_libdir} -type f -name \*.la -delete

mkdir -p %{buildroot}/%{_udevrulesdir}/
install -m 0644 -D -t %{buildroot}/%{_udevrulesdir}/ %{SOURCE1}

%files
%doc README.md CHANGELOG.md
%license LICENSE
%{_libdir}/libsapi.so.*
%{_libdir}/libtcti-device.so.*
%{_libdir}/libtcti-socket.so.*
%{_udevrulesdir}/60-tpm-udev.rules

%package        devel
Summary:        Headers and libraries for building apps that use tpm2-tss
Requires:       %{name}%{_isa} = %{version}-%{release}

%description    devel
This package contains headers and libraries required to build applications that
use tpm2-tss.

%files devel
%{_includedir}/sapi/
%{_includedir}/tcti/
%{_libdir}/libsapi.so
%{_libdir}/libtcti-device.so
%{_libdir}/libtcti-socket.so
%{_libdir}/pkgconfig/sapi.pc
%{_libdir}/pkgconfig/tcti-device.pc
%{_libdir}/pkgconfig/tcti-socket.pc
%{_mandir}/man3/Init*Tcti.3*
%{_mandir}/man7/tcti-*.7*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Tue Apr 10 2018 Chris Tessmer <chris.tessmer@onyxpoint.com> - 1.3.0-4
- Re-package Fedora to port recent improvements back to EL7

* Fri Feb 23 2018 Javier Martinez Canillas <javierm@redhat.com> - 1.3.0-4
- Install udev rule for TPM character devices

* Wed Feb 21 2018 Javier Martinez Canillas <javierm@redhat.com> - 1.3.0-3
- Remove ExclusiveArch: %%{ix86} x86_64 directive

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.0-2
- Escape macros in %%changelog

* Fri Dec 08 2017 Javier Martinez Canillas <javierm@redhat.com> - 1.3.0-1
- Update to 1.3.0 release

* Wed Nov 29 2017 Javier Martinez Canillas <javierm@redhat.com> - 1.3.0-0.1.rc2
- Update to 1.3.0 release candidate 2 (RHBZ#1508870)
- Remove global pkg_prefix since now the upstream repo and package names match
- Update URLs to point to the new project location
- Remove -Wno-int-in-bool-context compiler flag since now upstream takes care
- Remove %%doc directive since README.md and CHANGELOG.md are not in the tarball
- Add patch to include a LICENSE since the generated tarball does not have it

* Mon Aug 28 2017 Javier Martinez Canillas <javierm@redhat.com> - 1.2.0-1
- Update to 1.2.0 release
- Use tpm2-tss instead of TPM2.0-TSS as prefix since project name changed
- Fix SPEC file access mode
- Include new man pages in %%files directive

* Fri Aug 18 2017 Javier Martinez Canillas <javierm@redhat.com> - 1.1.0-3
- Remove unneeded source tarballs (RHBZ#1482828)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-1
- Update to 1.1.0 release

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Sun Yunying <yunying.sun@intel.com> - 1.0-2
- Remove global macro pkg_version to avoid duplicate of version
- Use ExclusiveArch instead of ExcludeArch
- Use less wildcard in %%files section to be more specific
- Add trailing slash at end of added directory in %%file section
- Remove autoconf/automake/pkgconfig(cmocka) from BuildRequires
- Increase release version to 2

* Fri Dec 2 2016 Sun Yunying <yunying.sun@intel.com> - 1.0-1
- Initial version of the package
