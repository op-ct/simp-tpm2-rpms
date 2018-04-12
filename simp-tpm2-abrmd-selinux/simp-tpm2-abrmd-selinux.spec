# defining macros needed by SELinux
%global selinuxtype targeted
%global selinux_policyver 0.0.1
%global moduletype contrib
%global modulename tabrmd

Name: simp-tpm2-abrmd-selinux
Version: 1.2.0
Release: 1%{?dist}
Summary: SELinux policies for tpm2-abrmd

License: BSD
URL:     https://github.com/tpm2-software/tpm2-abrmd
#Source0: https://github.com/tpm2-software/tpm2-abrmd/archive/%%{version}/tpm2-abrmd-%%{version}.tar.gz
Source0: %{name}-%{version}.tar.gz

BuildArch: noarch
Requires: selinux-policy >= %{selinux_policyver}
BuildRequires: git
BuildRequires: pkgconfig(systemd)
BuildRequires: selinux-policy
BuildRequires: selinux-policy-devel
Requires(post): selinux-policy-base >= %{selinux_policyver}
Requires(post): libselinux-utils
Requires(post): policycoreutils
%if 0%{?fedora}
Requires(post): policycoreutils-python-utils
%else
Requires(post): policycoreutils-python
%endif

%description
SELinux policy modules for product.

%prep
%setup -q -n %{name}-%{version}

%build
pushd selinux
%make_build TARGET="%{modulename}" SHARE="%{_datadir}"
popd

%pre
%selinux_relabel_pre -s %{selinuxtype}

%install
# install policy modules
pushd selinux
install -d %{buildroot}%{_datadir}/selinux/packages
install -d -p %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}
install -p -m 644 %{modulename}.if %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}
install -m 0644 %{modulename}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages
popd

%check

%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{modulename}.pp.bz2

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
fi

%posttrans
%selinux_relabel_post -s %{selinuxtype}

%files
%defattr(-,root,root,0755)
%attr(0644,root,root) %{_datadir}/selinux/packages/%{modulename}.pp.bz2
%attr(0644,root,root) %{_datadir}/selinux/devel/include/%{moduletype}/%{modulename}.if

%changelog
* Thu Mar 01 2018 Javier Martinez Canillas <javierm@redhat.com> - 0.0.1-1
- Initial packaging
