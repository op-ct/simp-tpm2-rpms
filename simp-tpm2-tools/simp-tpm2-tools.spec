Name: simp-tpm2-tools
Version: 3.0.3
Release: 3%{?dist}
Summary: A TPM2.0 testing tool build upon TPM2.0-TSS

# SIMP customization:
%define _prefix /usr/local

License: BSD
URL:     https://github.com/tpm2-software/tpm2-tools
#Source0: https://github.com/tpm2-software/tpm2-tools/releases/download/%{version}/%{name}-%{version}.tar.gz
Source0: %{name}-%{version}.tar.gz

BuildRequires: gcc-c++
BuildRequires: libtool
BuildRequires: pandoc
BuildRequires: autoconf-archive
BuildRequires: pkgconfig(cmocka)
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(openssl)
# tpm2-tss-devel provides sapi/tcti-device/tcti-socket
BuildRequires: pkgconfig(sapi)
BuildRequires: pkgconfig(tcti-device)
BuildRequires: pkgconfig(tcti-socket)
BuildRequires: pkgconfig(tcti-tabrmd)

# tpm2-tools is heavily depending on TPM2.0-TSS project, matched tss is required
Requires: simp-tpm2-tss%{?_isa} >= 1.3.0-1%{?dist}

# tpm2-tools project changed the install path for binaries and man page section
Obsoletes: simp-tpm2-tools <= 2.1.1-2


%description
tpm2-tools is a batch of testing tools for tpm2.0. It is based on tpm2-tss.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{_libdir}/pkgconfig ./bootstrap
PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{_libdir}/pkgconfig %configure \
  --disable-static --disable-silent-rules --with-tcti-socket \
  --with-tcti-device
%make_build

%install
%make_install

%files
%doc README.md CHANGELOG.md
%license LICENSE
%{_bindir}/tpm2_*
%{_mandir}/man1/tpm2_*.1*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Mon Apr 9 2018 Chris Tessmer <chris.tessmer@onyxpoint.com> - 3.0.3-3
- Tweak RPM for building EL7 RPMs

* Wed Feb 21 2018 Javier Martinez Canillas <javierm@redhat.com> - 3.0.3-3
- Remove ExclusiveArch: x86_64 directive

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 16 2018 Javier Martinez Canillas <javierm@redhat.com> - 3.0.3-1
- Update to 3.0.3 release

* Mon Dec 18 2017 Javier Martinez Canillas <javierm@redhat.com> - 3.0.2-1
- Update to 3.0.2 release

* Tue Dec 12 2017 Javier Martinez Canillas <javierm@redhat.com> - 3.0.1-1
- Update to 3.0.1 release (RHBZ#1512743)
- Download the generated tarball provided instead of the source code tarball

* Fri Dec 08 2017 Javier Martinez Canillas <javierm@redhat.com> - 3.0-1
- Update to 3.0 release

* Wed Nov 29 2017 Javier Martinez Canillas <javierm@redhat.com> - 3.0-0.1.rc1
- Update to 3.0 release candidate 1
- Update URLs to point to the new project location
- Make the package to obsolete version 2.1.1

* Wed Nov 01 2017 Javier Martinez Canillas <javierm@redhat.com> - 2.1.1-1
- Rename remaining tpm2.0-tools prefixes to tpm2-tools
- Remove global pkg_prefix since now the upstream repo and package names match
- Remove downstream patches since now these are in the latest upstream release
- Update to 2.1.1 release (RHBZ#1504438)

* Thu Oct 19 2017 Jerry Snitselaar <jsnitsel@redhat.com> - 2.1.0-7
- Clean up potential memleak (RHBZ#1503959)

* Thu Oct 05 2017 Javier Martinez Canillas <javierm@redhat.com> - 2.1.0-6
- Add tpm2-abrmd-devel BuildRequires so tools have abrmd support (RHBZ#1498909)

* Fri Aug 18 2017 Javier Martinez Canillas <javierm@redhat.com> - 2.1.0-5
- Remove unneeded source tarballs (RHBZ#1482830)

* Tue Aug 15 2017 Sun Yunying <yunying.sun@intel.com> - 2.1.0-4
- Add patch to fix build error when openssl-devel is installed(RHBZ#1481236)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Sun Yunying <yunying.sun@intel.com> - 2.1.0-2
- Add patch to fix gcc7 complaining about implicit-fallthrough cases

* Fri Jul 28 2017 Sun Yunying <yunying.sun@intel.com> - 2.1.0-1
- Update to latest upstream release 2.1.0

* Fri Jul 28 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-9
- Update Requires dependency so that tpm2-tss update won't break tpm2-tools

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 10 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-7
- Only update release version to make fedpkg build works for f26

* Wed Mar 1 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-6
- Update tpm2-tss version to 1.0-3 to fix broken dependency on f26

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 20 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-4
- Dependency check failed for Requires again, here to fix this
- Update release version and changelog

* Thu Jan 19 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-3
- Change spec file permission to 644 to avoid rpmlint complain
- Update Requires to fix dependency check error reported in Bodhi
- Remove tpm2-tss-devel version in BuildRequires comment
- Update release version and changelog

* Wed Dec 21 2016 Sun Yunying <yunying.sun@intel.com> - 1.1.0-2
- Remove pkg_version to avoid dupliate use of version
- Remove redundant BuildRequires for autoconf/automake/pkgconfig
- Add comments for BuildRequires of sapi/tcti-device/tcti-socket
- Use ExclusiveArch instead of ExcludeArch
- Requires tpm2-tss version updated to 1.0-2
- Updated release version and changelog

* Fri Dec 2 2016 Sun Yunying <yunying.sun@intel.com> - 1.1.0-1
- Initial version of the package
