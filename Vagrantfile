# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "bento/ubuntu-20.04"
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.provision "bootstrap", type: "shell", privileged: false do |s|
    s.inline = "bash /vagrant/remote-setup/setup.sh"
  end
end
