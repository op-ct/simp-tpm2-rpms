#!/bin/bash

rvm use 2.1.9
sudo yum erase simp\* -y; :

cd /vagrant
cd simp-tpm2-tss/ && \
bundle exec rake clean && bundle exec rake pkg:rpm && sudo yum install dist/simp-tpm2-*.rpm -y && \
cd ../simp-tpm2-abrmd-selinux/ && \
bundle exec rake clean && bundle exec rake pkg:rpm && sudo yum install dist/simp-tpm2-*.rpm -y
cd ../simp-tpm2-abrmd/ && \
bundle exec rake clean && bundle exec rake pkg:rpm && sudo yum install dist/simp-tpm2-*.rpm -y && \
cd ../simp-tpm2-tools/ && \
bundle exec rake clean && bundle exec rake pkg:rpm && sudo yum install dist/simp-tpm2-*.rpm -y
cd ..


TMPFILE=$(mktemp -t rebuild.sh.XXXXXXXXXX || exit 1)
cat > "${TMPFILE}"<<SYSTEMD
[Service]
ExecStart=
ExecStart=/usr/local/sbin/tpm2-abrmd -t socket
SYSTEMD

sudo mkdir -p /etc/systemd/system/tpm2-abrmd.service.d
sudo cp "${TMPFILE}" /etc/systemd/system/tpm2-abrmd.service.d/override.conf
sudo chmod 0644 /etc/systemd/system/tpm2-abrmd.service.d/override.conf
sudo systemctl daemon-reload
sudo restorecon /usr/local/sbin/tpm2-abrmd
sudo systemctl enable tpm2-abrmd.service
sudo systemctl start tpm2-abrmd.service
sudo udevadm control --reload-rules && sudo udevadm trigger
