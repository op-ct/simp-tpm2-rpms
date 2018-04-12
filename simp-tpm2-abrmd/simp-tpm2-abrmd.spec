%global selinuxtype targeted
%global selinux_policyver 3.13.1-166
%global moduletype contrib
%global modulename tabrmd
# SIMP customization:
%global _prefix /usr/local
%global _selinux_share /usr/share
Name: simp-tpm2-abrmd
Version: 1.2.0
Release: 0%{?dist}
Summary: A system daemon implementing TPM2 Access Broker and Resource Manager


License: BSD
URL:     https://github.com/01org/tpm2-abrmd
### Source0: https://github.com/01org/tpm2-abrmd/archive/%%{version}/%%{name}-%%{version}.tar.gz
Source0: %{name}-%{version}.tar.gz
# upstream commit 418d49669a33f9e6b029787e3869b3a534bb7de8
#Patch0: 0001-tcti-tabrmd-Fix-NULL-deref-bug-by-moving-debug-outpu.patch


%{?systemd_requires}
# tpm2-abrmd depends on tpm2-tss for sapi/tcti-device/tcti-socket libs
BuildRequires: simp-tpm2-tss-devel >= 1.1.0-1%{?dist}
BuildRequires: systemd
BuildRequires: libtool
BuildRequires: autoconf-archive
BuildRequires: pkgconfig(cmocka)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(sapi)
BuildRequires: pkgconfig(tcti-device)
BuildRequires: pkgconfig(tcti-socket)

%description
tpm2-abrmd is a system daemon implementing the TPM2 access broker (TAB) and
Resource Manager (RM) spec from the TCG.

%prep
%autosetup -p1 -n %{name}-%{version}
autoreconf -vif
./bootstrap
PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{_libdir}/pkgconfig %configure --disable-static --disable-silent-rules \
           --with-systemdsystemunitdir=%{_unitdir} \
           --with-udevrulesdir=%{_udevrulesdir}

%build
%make_build

%install
%make_install
rm -f %{buildroot}/%{_udevrulesdir}/tpm-udev.rules
find %{buildroot}%{_libdir} -type f -name \*.la -delete

%pre
mkdir -p %{_datadir}

getent group tss >/dev/null || groupadd -g 59 -r tss
getent passwd tss >/dev/null || \
useradd -r -u 59 -g tss -d /dev/null -s /sbin/nologin \
 -c "Account used by the tpm2-abrmd package to sandbox the tpm2-abrmd daemon" tss
exit 0


%post
# Make sure our %%{_libdir} is in the library path
echo "%{_libdir}" > /etc/ld.so.conf.d/tpm2-abrmd.conf
chmod 644 /etc/ld.so.conf.d/tpm2-abrmd.conf
/sbin/ldconfig

udevadm trigger

%systemd_post tpm2-abrmd.service

# restart the dbus daemon to load the dbus configuration updates
pkill -HUP dbus-daemon

%preun
%systemd_preun tpm2-abrmd.service

%postun
rm -f /etc/ld.so.conf.d/tpm2-abrmd.conf
/sbin/ldconfig
%systemd_postun tpm2-abrmd.service

%files
%doc README.md CHANGELOG.md
%license LICENSE
%{_libdir}/libtcti-tabrmd.so.*
%{_libdir}/systemd/system-preset/tpm2-abrmd.preset
%{_sbindir}/tpm2-abrmd
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/tpm2-abrmd.conf
%{_unitdir}/tpm2-abrmd.service
%{_mandir}/man3/tss2_tcti_tabrmd_init.3*
%{_mandir}/man3/tss2_tcti_tabrmd_init_full.3*
%{_mandir}/man7/tcti-tabrmd.7*
%{_mandir}/man8/tpm2-abrmd.8*


# ------------------------------------------------------------------------------
%package devel
Summary: Headers, static libraries and package config files of tpm2-abrmd
Requires: %{name}%{_isa} = %{version}-%{release}
# tpm2-abrmd-devel depends on tpm2-tss-devel for sapi/tcti-device/tcti-socket libs
Requires: simp-tpm2-tss-devel%{?_isa} >= 1.1.0-1%{?dist}

%description devel
This package contains headers, static libraries and package config files
required to build applications that use tpm2-abrmd.

%files devel
%{_includedir}/tcti/tcti-tabrmd.h
%{_libdir}/libtcti-tabrmd.so
%{_libdir}/pkgconfig/tcti-tabrmd.pc

# ------------------------------------------------------------------------------
%changelog
* Tue Apr 10 2018 Chris Tessmer <chris.tessmer@onyxpoint.com> - 1.2.0-0
- Re-package Fedora to port recent improvements back to EL7

* Fri Feb 23 2018 Javier Martinez Canillas <javierm@redhat.com> - 1.1.0-12
- Don't install udev rule for TPM character devices

* Fri Feb 23 2018 Javier Martinez Canillas <javierm@redhat.com> - 1.1.0-12
- Don't install udev rule for TPM character devices

* Wed Feb 21 2018 Javier Martinez Canillas <javierm@redhat.com> - 1.1.0-11
- Remove ExclusiveArch: x86_64 directive

* Thu Feb 15 2018 Javier Martinez Canillas <javierm@redhat.com> - 1.1.0-10
- Remove %%{_isa} from BuildRequires (RHBZ#1545210)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Oct 25 2017 Peter Jones <pjones@redhat.com> - 1.1.0-8
- Make only tpm2-abrmd-devel have a runtime dep on tpm2-tools-devel

* Wed Oct 18 2017 Jerry Snitselaar <jsnitsel@redhat.com> - 1.1.0-7
- tcti-abrmd: Fix null deref

* Fri Oct 13 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-6
- Add tss user if doesn't currently exist - PR#1 from Jerry Snitselaar
- Removed source tarball and cleared it from .gitignore

* Wed Aug 16 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-5
- Updated source0 URL to fix rpmlint warnings

* Tue Aug 15 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-4
- Rename and relocate udev rules file to _udevrulesdir
- Update scriptlet to add service name after systemd_postrun

* Tue Aug 1 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-3
- Use config option with-systemdsystemunitdir to set systemd unit file location

* Mon Jul 31 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-2
- Removed BuildRequires for gcc
- Move tpm2-abrmd systemd service to /usr/lib/systemd/system
- Added scriptlet for tpm2-abrmd systemd service
- Use autoreconf instead of bootstrap

* Wed Jul 26 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-1
- Initial packaging
