# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # For a complete reference of oconfiguration options, please see the online
  # documentation at https://docs.vagrantup.com.

  config.vm.box = "centos/7"

  config.vm.define ENV['VAGRANT_BOX_NAME'] || 'simp_tpm2_rpm_builder'

  config.vm.provision 'shell', inline: <<-SHELL

    yum install --enablerepo=extras -y vim-enhanced git libicu-devel \
                                       rpm-build rpmdevtools epel-release

    yum install --enablerepo=extras,epel -y haveged libmocka-devel selinux-policy-devel \
                                            git make autoconf autoconf-archive \
                                            automake libtool gcc gcc-c++ \
                                            glibc-headers pkgconfig openssl-devel \
                                            curl-devel \
                                            pkgconfig libcmocka-devel dbus-devel glib2-devel \
                                            pandoc

    # enable HAVEGED
    # --------------------
    # This gives the VM's /dev/*random sufficient entropy for all the crypto
    # in the build
    systemctl start haveged
    systemctl enable haveged

###    # Install docker
###    # --------------------
###    yum install --enablerepo=extras,epel -y docker
###
###    # You can also append `-G vagrant` to `OPTIONS=` in /etc/sysconfig/docker
###     cat <<DOCKAH > /etc/docker/daemon.json
### {
### "live-restore": true,
### "group": "vagrant"
### }
### DOCKAH
###
###    # man docker-storage-setup
###    # https://bugzilla.redhat.com/show_bug.cgi?id=1316210
###    echo 'EXTRA_STORAGE_OPTIONS="--storage-opt overlay2.override_kernel_check=true"' >> /etc/sysconfig/docker-storage-setup
###    container-storage-setup
###    systemctl start docker
###    systemctl enable docker
###
###    chown -R vagrant /vagrant # TODO: why is this needed?
###    ls -lartZ /var/run/docker.sock
  SHELL


  # pass on certain environment variables from the `vagrant CMD` cli to the
  # rake task run it the VM
  _bash_env_string = (
    ENV
     .to_h
     .select{ |k,v| k =~ /^SIMP_.*|^BEAKER_.*|RSYNC_NO_SELINUX_DEPS/ }
     .map{|k,v| "#{k}=#{v}"}
  )
  bash_env_string = _bash_env_string.join(' ')

  config.vm.provision 'shell', privileged: false, inline: <<-SHELL
    cd /vagrant

    cat <<ENV > /vagrant/.env
#{_bash_env_string.join("\n")}
ENV
    [ "${SIMP_BUILDER_install_rvm:-yes}" == yes ] || { echo "== skipping ${0}: SIMP_BUILDER_install_rvm='${SIMP_BUILDER_install_rvm}' (instead of 'yes')"; }

    # Install RVM
    gpg2 --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
    [ -f install_rvm.sh ] || curl -sSL https://get.rvm.io > install_rvm.sh
    bash install_rvm.sh stable '--with-default-gems=beaker rake'
    source /home/vagrant/.rvm/scripts/rvm
    rvm install --disable-binary ruby-2.1.9
    gem install bundler --no-ri --no-rdoc

    cd /vagrant
    [[ -f Gemfile ]] && #{bash_env_string} bundle

    # getting lazy, and building the simulator without an RPM:
    # build
    pgrep tpm_server &> /dev/null

    if [ $? -ne 0 ]; then
      sudo yum install -y wget
      wget wget https://downloads.sourceforge.net/project/ibmswtpm2/ibmtpm974.tar.gz
      mkdir ibmtpm974
      cd ibmtpm974/
      tar -xavf ../ibmtpm974.tar.gz
      cd src
      make
      # start
      cp tpm_server /vagrant/
      cd /vagrant
      ./tpm_server -rm &> /vagrant/tpm_server.$(date +%Y%m%d.%H%M).log &

      [ $? -ne 0 ] && { echo "FAIL: ibmswtpm2 failed to start" && exit 1; }
    fi

    # TODO: build in docker
    bash /vagrant/rebuild.sh

    sudo rpm -Uvh https://yum.puppetlabs.com/puppetlabs-release-pc1-el-7.noarch.rpm
    sudo yum install puppet-agent
    sudo /opt/puppetlabs/bin/puppet module install simp-tpm
    sudo rm -rf /etc/puppetlabs/code/environments/production/modules/tpm
    sudo git clone https://github.com/simp/pupmod-simp-tpm.git /etc/puppetlabs/code/environments/production/modules/tpm
    sudo /opt/puppetlabs/bin/puppet module list --tree
SHELL
end
