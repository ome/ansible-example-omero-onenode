# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"
  # config.vm.box = "ubuntu/bionic64"

  config.vm.hostname = "omero-all"

  config.vm.network "private_network", type: "dhcp"
  config.vm.network "private_network", ip: "192.168.33.12"

  config.vm.provider "virtualbox" do |vb|
    # vb.gui = true
    vb.cpus = 2
    vb.memory = "4096"
  end

  # Allow SSH with your own key
  # https://stackoverflow.com/a/36865927
  ssh_pub_key = File.readlines("#{Dir.home}/.ssh/id_rsa.pub").first.strip
  config.vm.provision 'shell', inline: "echo #{ssh_pub_key} >> /home/vagrant/.ssh/authorized_keys", privileged: false  
end
