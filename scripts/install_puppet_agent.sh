#!/bin/bash

sudo rpm -Uvh https://yum.puppetlabs.com/puppetlabs-release-pc1-el-7.noarch.rpm
sudo yum install puppet-agent -y
sudo /opt/puppetlabs/bin/puppet module install simp-tpm
sudo rm -rf /etc/puppetlabs/code/environments/production/modules/tpm; :
sudo git clone https://github.com/simp/pupmod-simp-tpm.git /etc/puppetlabs/code/environments/production/modules/tpm
sudo /opt/puppetlabs/bin/puppet module list --tree
