%define module_name can
%define kernel_versions 5.0
%define license GPL-2.0


%{?!module_name: %{error: You did not specify a module name (%%module_name)}}
%{?!kernel_versions: %{error: You did not specify kernel versions (%%kernel_version)}}
%{?!packager: %define packager Ronan Le Martret  <ronan.lemartret@iot.bzh>}
%{?!license: %define license Unknown}
%{?!_dkmsdir: %define _dkmsdir /var/lib/dkms}
%{?!_srcdir: %define _srcdir %_prefix/src}
%{?!_datarootdir: %define _datarootdir %{_datadir}}

Summary:	%{module_name}-dkms %{version} dkms package
Name:		%{module_name}-dkms
Version:	5.0
License:	%license
Release:	1dkms
BuildArch:	noarch
Group:		System/Kernel
Requires: 	dkms >= 1.95
Requires: 	dkms
Requires: 	kernel-devel >= 5.0
BuildRoot: 	%{_tmppath}/%{name}-dkms-%{version}-%{release}-root/

Source:	%{name}-%{version}.tar.gz
Source2:	common.postinst

%description
Kernel modules for %{module_name} %{version} in a DKMS wrapper.

%prep
%setup -q -n %{name}-%{version}

%build

%install

mkdir -p %{?buildroot}/%{_srcdir}
mkdir -p %{?buildroot}/%{_datarootdir}/%{module_name}

mkdir -p %{?buildroot}/%{_srcdir}/%{module_name}-%{version}
cp -fpr * %{?buildroot}/%{_srcdir}/%{module_name}-%{version}
install -m 755 %{SOURCE2} %{?buildroot}/%{_datarootdir}/%{module_name}/postinst

%clean
if [ "%{?buildroot}" != "/" ]; then
        rm -rf %{?buildroot}
fi

%post
for POSTINST in %{_prefix}/lib/dkms/common.postinst %{_datarootdir}/%{module_name}/postinst; do
        if [ -f $POSTINST ]; then
                $POSTINST %{module_name} %{version} %{_datarootdir}/%{module_name}
                exit $?
        fi
        echo "WARNING: $POSTINST does not exist."
done
echo -e "ERROR: DKMS version is too old and %{module_name} was not"
echo -e "built with legacy DKMS support."
echo -e "You must either rebuild %{module_name} with legacy postinst"
echo -e "support or upgrade DKMS to a more current version."
exit 1

%preun
echo -e
echo -e "Uninstall of %{module_name} module (version %{version}) beginning:"
dkms remove -m %{module_name} -v %{version} --all --rpm_safe_upgrade
exit 0

%files
%defattr(-,root,root)
%{_srcdir}
%{_datarootdir}/%{module_name}/

%changelog
* Fri Oct 25 15:30:57 CEST 2019 Ronan Le Martret <ronan.lemartret@iot.bzh> %{version}-%{release}
- Build by IoT.bzh

