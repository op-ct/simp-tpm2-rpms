#!/bin/bash

rvm use 2.1.9
cd /vagrant

sudo yum  erase simp\* -y; :

    cd simp-tpm2-tss/ && \
    bundle exec rake clean && bundle exec rake pkg:rpm && sudo yum install dist/simp-tpm2-*.rpm -y && \
    cd ../simp-tpm2-abrmd/ && \
    bundle exec rake clean && bundle exec rake pkg:rpm && sudo yum install dist/simp-tpm2-*.rpm -y && \
    cd ../simp-tpm2-tools/ && \
    bundle exec rake clean && bundle exec rake pkg:rpm && sudo yum install dist/simp-tpm2-*.rpm -y
    cd ..
