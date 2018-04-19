Name: simp-tpm2-simulator
Version: 1119.0.0
Release: 0%{?dist}
Summary: The IBM TPM2.0 simulator

# SIMP customization:
%define _prefix /usr/local

License: BSD
URL:     https://sourceforge.net/projects/ibmswtpm2/
###https://sourceforge.net/projects/ibmswtpm2/files/ibmtpm%%{version}.tar.gz/download
Source0: %{name}-%{version}.tar.gz

BuildRequires: gcc-c++
BuildRequires: pkgconfig(openssl)


%description
IBM's simulator that implements the TCG TPM 2.0 specification. It is based on
the TPM specification Parts 3 and 4 source code donated by Microsoft, with
additional files to complete the implementation.

%prep
%setup -q %{SOURCE0}

%build
cd src/
%make_build

%install
mkdir -p %{buildroot}/%{_bindir}
cp -p src/tpm_server  %{buildroot}/%{_bindir}/tpm2-simulator

%files
%doc ibmtpm.doc
%license LICENSE
%{_bindir}/tpm2-*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Mon Apr 9 2018 Chris Tessmer <chris.tessmer@onyxpoint.com> - 3.0.3-3
- Tweak RPM for building EL7 RPMs

* Tue Dec 12 2017 XXX <x.x@x.x> - 1119.0.0-0
- Support for OpenSSL 1.1.x.
- Support for big endian platforms, using BIG_ENDIAN_TPM=YES
- An update to TPM specification draft revision 146
  - avalable for public review
  - includes changes to TPM2_CreateLoaded and TPM2_EncryptDecrypt
- Support for Nuvoton TPM vendor specific commands
- A contributed makefile.mac for Mac
- The TPM starts powered up, so the initial power up command is not necessary
- Non-deterministic random numbers are used when SIMULATION is not set
- A few tweaks for better cygwin support

* Tue Mar 21 2017 XXX <x.x@x.x> - 974.0.0-0
- An update to the TPM specification draft revision 142, with errata to
  revision 138.

* Fri Nov 18 2016 XXX <x.x@x.x> - 832.0.0-0
- The TPM state NVChip is not compatible with previous builds.
  - Remove NVChip before running the first time.
- An update to TPM specification revision 138.
  - 138 includes 4 new commands and a refactoring of the crypto code to make it
    easier to replace the crypto library.

* Mon Apr 11 2016 XXX <x.x@x.x> - 523.0.0-0
- A possible fix to the reported platform port number race condition.

* Wed Dec 23 2015 XXX <x.x@x.x> - 477.0.0-0
- An update to TPM 2.0 draft specification revision 124
- A command line parameter to force remanufacturing. The previous release
  performed manufacturing each time the simulator was started. All NV memory
  was initialized. By default, without the new command line parameter, this
  build retains NV state.

