# Overview

This repository contains everything needed to build RPM's for [Prometheus Node Exporter](https://github.com/prometheus/node_exporter) . The .spec file has been tested on EL7, EL8, SLES12 and SLES15.

## Prepare

Ensure packages are installed that provide tools to build the source and binary rpms.

#### SuSE

- `sudo zypper install -y rpm-build rpmdevtools`

#### Red Hat

- `sudo yum install -y rpm-build rpmdevtools`

## Building

1. `git clone https://github.com/mzima/node_exporter-rpms`
2. `cd node_exporter-rpms`
3. `rpmdev-setuptree`
4. `wget -P SOURCES/ https://github.com/prometheus/node_exporter/releases/download/v1.0.1/node_exporter-1.0.1.linux-amd64.tar.gz`
4. `rpmbuild -ba --nodeps --define "_sourcedir $(pwd)" --define "_srcrpmdir $(pwd)" --define "_rpmdir $(pwd)/.." node_exporter.spec`

The source and binary rpm files can be found in the node_exporter-rpms directory after the rpmbuild finishes.

## Start/Stop Node Exporter service

```
# systemctl start node_exporter
# systemctl status node_exporter
● node_exporter.service - Prometheus Node Expoter
     Loaded: loaded (/usr/lib/systemd/system/node_exporter.service; disabled; vendor preset: disabled)
     Active: active (running) since Mon 2021-01-25 21:52:50 CET; 31min ago
   Main PID: 4673 (node_exporter)
      Tasks: 4 (limit: 1126)
     Memory: 8.5M
     CGroup: /system.slice/node_exporter.service
             └─4673 /usr/sbin/node_exporter --web.config=/etc/prometheus/node_exporter/web-config.yml --log.level=info
...
# systemctl stop node_exporter
```

## Accessing Node Exporter log files

Zookeepers logs are available in systemd's `journal` facility with `node_exporter` identifier and can be accessed as:

```
$ journalctl -t node_exporter
```

## Hardening Node Exporter

Prometheus Node Exporter supports TLS and/or HTTP basic auth since [v1.0.0](https://github.com/prometheus/exporter-toolkit/blob/v0.1.0/https/README.md).
The script **SOURCE/node_exporter-secure.py** can be used to automatically harden your Node Exporter installation by:

1. creating a self-signed TLS certificate and key
2. creating a random password for the connection user node_exporter
3. configure node_exporter to use tls and basic authentication

Please note, that the **node_exporter-secure.py** script is not part of the rpm package unless the parameter **_package_include_hardening_script** inside the .spec file is set to **1**. The script requires python3, python3-bcrypt (EPEL) and openssl.

### Usage:
```
# /usr/sbin/node_exporter-secure.py --yes --terse
node_exporter:CLEARTEXT_PASSWORD

# systemctl restart node_exporter
```

