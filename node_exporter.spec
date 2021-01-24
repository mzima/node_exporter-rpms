Name:      node_exporter
Version:   1.0.1
Release:   1
BuildArch: x86_64
Summary:   The Prometheus Node Exporter exposes a wide variety of hardware- and kernel-related metrics
License:   GPLv3
URL:       https://github.com/prometheus/node_exporter
Group:     System Environment/Daemons
Source0:   https://github.com/prometheus/node_exporter/releases/download/v%{version}/node_exporter-%{version}.linux-amd64.tar.gz
Source1:   %{name}.service
Source2:   %{name}-secure.py
Source3:   web-config.yml
Source4:   %{name}.sysconfig
Packager:  Martin Zimmermann <martin.zimmermann@fujitsu.com>
%define _base_sbin_dir %{_sbindir}
%define _base_etc_dir %{_sysconfdir}/prometheus/%{name}
%define _base_sysconfig_dir %{_sysconfdir}/sysconfig
%define _systemd_unit_name %{name}.service
%define _package_include_hardening_script 0

%if %{_package_include_hardening_script}
Requires:  python3, python3-bcrypt, python3-PyYAML, openssl
%endif

%description
The Prometheus Node Exporter exposes a wide variety of hardware- and kernel-related metrics.

%prep
%setup -n %{name}-%{version}.linux-amd64

%build
echo  %{buildroot}
rm -rf %{buildroot}

%install
install -d -m 755 %{buildroot}
install -d -m 755 %{buildroot}%{_base_sbin_dir}
install -d -m 755 %{buildroot}%{_base_etc_dir}
install -d -m 755 %{buildroot}%{_unitdir}
install -p -D -m 755 %{_builddir}/%{name}-%{version}.linux-amd64/%{name} %{buildroot}%{_base_sbin_dir}
install -p -D -m 644 %{S:1} %{buildroot}%{_unitdir}${_systemd_unit_name}
install -p -D -m 644 %{S:3} %{buildroot}%{_base_etc_dir}/web-config.yml
install -p -D -m 644 %{S:4} %{buildroot}%{_base_sysconfig_dir}/%{name}
%if %{_package_include_hardening_script}
install -p -D -m 755 %{S:2} %{buildroot}%{_base_sbin_dir}/%{name}-secure.py
%endif

%files
%defattr(-,root,root)
%{_base_sbin_dir}/%{name}
%{_unitdir}/%{_systemd_unit_name}
%config(noreplace) %{_base_etc_dir}/web-config.yml
%config(noreplace) %{_base_sysconfig_dir}/%{name}
%if %{_package_include_hardening_script}
%{_base_sbin_dir}/%{name}-secure.py
%endif

%clean
rm -rf %{buildroot}

%pre
%service_add_pre %{_systemd_unit_name}

%post
%service_add_post %{_systemd_unit_name}

%preun
%service_del_preun %{_systemd_unit_name}

%postun
%service_del_postun %{_systemd_unit_name}

%changelog
