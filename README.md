# Install OMERO on CentOS 7 or Ubuntu 18.04 using Ansible

1. Install Ansible.
   For instance, you can use a Python virtualenv::
    ```
    python3 -mvenv ansible-venv
    . ansible-venv/bin/activate
    python3 -mpip install ansible
    ```
   A conda environment
    ```
    conda create -n ansible ansible
    conda activate ansible
    ```
   or some other package manager.
2. Edit `ansible_host` in [`inventory.yml`](inventory.yml) to point to the server you wish to install OMERO on.
3. Check you can SSH into the server, and that you can run `sudo`.
4. Install the required Ansible roles:
```
ansible-galaxy install -p roles -r requirements.yml
```
5. Run `ansible-playbook`:
```
ansible-playbook -i inventory.yml playbook.yml
```
Use `playbook.yml` for CentOS 7 and `playbook-ubuntu.yml` for Ubuntu 18.04.
If necessary you can specify the user to login with: `-u USERNAME`.
If you do not have passwordless sudo setup pass `--ask-become-pass`.
For verbose output pass `-v`, `-vv` or `-vvv`.

Login to OMERO with username `root` password `ChangeMe`.


## Testing with Vagrant and VirtualBox

If you have [Vagrant](https://www.vagrantup.com/) and [Virtualbox](https://www.vagrantup.com/docs/providers/virtualbox) installed you can easily spin up a virtual machine to try out the Ansible playbook.
1. Edit `config.vm.box` in [`Vagrantfile`](Vagrantfile) to choose your operating system, either Centos 7 (default) or Ubuntu 18.04.
This includes networking configuration that means your virtual machine will be listening on `192.168.33.12`.
2. Start the virtual machine:
    ```
    vagrant up
    ```
3. Install roles as above, then run `ansible-playbook`:
    ```
    ansible-playbook -i inventory.yml playbook.yml -u vagrant
    ```
