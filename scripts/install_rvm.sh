#!/bin/bash

gpg2 --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
[ -f install_rvm.sh ] || curl -sSL https://get.rvm.io > install_rvm.sh
bash install_rvm.sh stable '--with-default-gems=beaker rake'
source /home/vagrant/.rvm/scripts/rvm
rvm install --disable-binary ruby-2.1.9
gem install bundler --no-ri --no-rdoc
