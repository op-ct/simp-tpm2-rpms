# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # For a complete reference of oconfiguration options, please see the online
  # documentation at https://docs.vagrantup.com.

  config.vm.box = "centos/7"

  config.vm.define (ENV['VAGRANT_BOX_NAME'] || 'simp_tpm2_rpm_builder') do |vm|

    vm.vm.synced_folder '.', '/vagrant',
                       create: true,
                       type:   'rsync',
                       rsync_exclude: '.git/',
                       rsync__verbose: true,
                       rsync__chown: true




    vm.vm.provision 'shell', inline: <<-SHELL

      yum install --enablerepo=extras -y vim-enhanced git libicu-devel \
                                         rpm-build rpmdevtools epel-release \
                                         wget

      yum install --enablerepo=extras,epel -y haveged selinux-policy-devel \
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

    vm.vm.provision 'shell', privileged: false, inline: <<-NONPRIV_SHELL

      # Persist env vars
      if [ -n "#{_bash_env_string.join('-')}" ]; then
        cat <<ENV > /vagrant/.env
#{_bash_env_string.join("\n")}

#{_bash_env_string.map{|x| 'export ' + x.gsub(/=.*$/,'') }.join("\n")}
ENV
        . /vagrant/.env
      fi

      source /vagrant/scripts/install_rvm.sh

      cd /vagrant
      [[ -f Gemfile ]] && #{bash_env_string} bundle

      source /vagrant/scripts/build_tpm2_sim.sh && \\
      source /vagrant/scripts/rebuild_tpm2_rpms.sh && \\
      source /vagrant/scripts/install_puppet_agent.sh

    NONPRIV_SHELL

  end
end
