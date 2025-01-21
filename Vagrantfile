Vagrant.configure("2") do |config|
  config.vm.hostname = "cloud"

  # Use the Docker provider because it is faster and more lightweight
  # qemu is the only other provider that plays well with x86_64 and arm64 and that is slow
  config.vm.provider :docker do |docker, override|
    override.vm.box = nil
    docker.image = "rofrano/vagrant-provider:ubuntu"
    docker.remains_running = true
    docker.has_ssh = true
    docker.privileged = true

    # only mount cgroup if we are on Linux/OSX
    docker.volumes << "/sys/fs/cgroup:/sys/fs/cgroup:rw"
    docker.create_args = ["--cgroupns=host"]

    # sync the code, tests, and pyproject.toml into the container
    docker.volumes << "./cc_simple_server:/home/vagrant/app/cc_simple_server:rw"
    docker.volumes << "./pyproject.toml:/home/vagrant/app/pyproject.toml:rw"
    docker.volumes << "./tests:/home/vagrant/app/tests:rw"
  end

  # use Virtualbox for x86 (Windows or older Macs)
  config.vm.provider :virtualbox do |vb, override|
    override.vm.box = "ubuntu/jammy64"
    vb.memory = 2048
    vb.cpus = 2

    # sync the world
    override.vm.synced_folder ".", "/home/vagrant/app", owner: "vagrant", group: "vagrant"
  end

  # network setup
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  # inline shell script to setup the environment
  config.vm.provision "shell", inline: <<-SHELL
    echo "🌟 Setting up FastAPI Development Environment! 🌟"

    # update and install
    apt-get update
    apt-get install -y software-properties-common curl python3.11 python3.11-venv python3.11-dev python3-pip build-essential sudo

    # make vagrant a sudoer
    if id "vagrant" &>/dev/null; then
      usermod -aG sudo vagrant
      echo "vagrant ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
    else
      echo "User 'vagrant' not found, skipping sudo group addition"
    fi

    # set ownership and permissions
    chown -R vagrant:vagrant /home/vagrant/app
    chmod -R u+rwx /home/vagrant/app

    # python3.11
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
    update-alternatives --set python3 /usr/bin/python3.11

    sudo -H -u vagrant sh -c 'curl -sSL https://install.python-poetry.org | python3.11 -'
    sudo -H -u vagrant sh -c 'export PATH="$HOME/.local/bin:$PATH"'
    sudo -H -u vagrant sh -c 'cd /home/vagrant/app/ && /home/vagrant/.local/bin/poetry install --no-root'

    # Add PYTHONPATH for pytest oh boy
    echo 'export PYTHONPATH="/home/vagrant/app"' >> /home/vagrant/.bashrc
    export PYTHONPATH="/home/vagrant/app"

    echo "✅ Setup complete! Start your FastAPI app running the following:"
    echo "  vagrant ssh"
    echo "vagrant@cloud:~$ cd app"
    echo "vagrant@cloud:~/app$ poetry run uvicorn cc_simple_server.server:app --reload --host 0.0.0.0 --port 8000"
  SHELL
end
