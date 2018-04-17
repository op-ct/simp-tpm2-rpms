#!/bin/bash
#
# The lazy/quick way of:
#
#   * building the TPM2 simulator without an RPM, and
#   * running it without SELinux contexts
#
# TODO: provide RPM + selinux contexts

pgrep tpm_server &> /dev/null

if [ $? -ne 0 ]; then

  if [ -f /vagrant/tpm_server ] && [ -x /vagrant/tpm_server ]; then
    echo "INFO: /vagrant/tpm_server already exists―using"
  else
    # build
    wget wget https://downloads.sourceforge.net/project/ibmswtpm2/ibmtpm974.tar.gz
    mkdir -p ibmtpm974
    cd ibmtpm974/
    tar -xavf ../ibmtpm974.tar.gz
    cd src
    make clean && make && cp -v tpm_server /vagrant/
  fi

  # start
  echo "== starting /vagrant/tpm_server"

  cd /vagrant
  /vagrant/tpm_server -rm &> "/vagrant/tpm_server.$(date +%Y%m%d.%H%M).log" &
  [ $? -ne 0 ] && { echo "FAIL: ibmswtpm2 failed to start" && exit 1; }
fi

sleep 2
pgrep tpm_server &> /dev/null
