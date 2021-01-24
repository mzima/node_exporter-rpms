#!/usr/bin/python3
#
# Prometheus node exporter hardening script
#

import bcrypt
import argparse
import string
import secrets
import os
import sys
import socket
import subprocess
import yaml

errors = False
conf_dir = "/etc/prometheus/node_exporter"
conf_file = "%s/web-config.yml" % conf_dir
ssl_dir = "%s/tls" % conf_dir
ssl_file_key = "%s/node_exporter.key" % ssl_dir
ssl_file_crt = "%s/node_exporter.cert" % ssl_dir
ssl_days = 1095
ssl_size = 2048
ssl_subj = "/O=Prometheus Node Exporter CA/CN=%s" % socket.getfqdn()
auth_user = "node_exporter"

# arg parse
parser = argparse.ArgumentParser()
parser.add_argument('-y', '--yes', action='store_true', help='confirm questions')
parser.add_argument('-t', '--terse', action='store_true', help='terse output')
args = parser.parse_args()

if not args.yes:
    confirm = input('Confirm to overwrite current TLS certs and config.yml (y/n) : ')
    if confirm[0].lower() != 'y':
        exit(2)

# generate a tls certificate
if not os.path.exists(ssl_dir):
    os.mkdir(ssl_dir)

cmd_ssl_create = "openssl req -new -newkey rsa:%i -days %i -nodes -x509 -keyout %s -out %s -subj \"%s\"" % (ssl_size, ssl_days, ssl_file_key, ssl_file_crt, ssl_subj)
if not args.terse:
    print("Create TLS keypair %s ..." % ssl_dir)
    subprocess.call(cmd_ssl_create, shell=True)
else:
    FNULL = open(os.devnull, 'w')
    subprocess.call(cmd_ssl_create, shell=True, stdout=FNULL, stderr=FNULL)

# generate a secure password hash
s = string.ascii_letters + string.digits
auth_pass = ''.join(secrets.choice(s) for i in range(16))
auth_salt = bcrypt.gensalt(rounds=8)
auth_hash = bcrypt.hashpw(auth_pass.encode('utf-8'), auth_salt).decode()

# generate file content
content_conf_file = {
    "tls_server_config": {
        "cert_file": ssl_file_crt,
        "key_file": ssl_file_key
    },
    "basic_auth_users": {
        auth_user: auth_hash
    }
}

if not args.terse:
    print("Create config file %s" % conf_file)

with open(conf_file, 'w') as f:
    documents = yaml.dump(content_conf_file, f, default_flow_style=False)

if not args.terse:
    print("\nHttp-auth user: %s" % auth_user)
    print("Http-auth pass: %s" % auth_pass)
else:
    print("%s:%s" % (auth_user, auth_pass))

