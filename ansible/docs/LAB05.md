# Task 2

### "First" run
(Not really the first, I tore the environment down manually).

```text
timur@timur-ficus:~/proj/DevOps-Core-Course/ansible$ ansible-playbook playbooks/provision.yml

PLAY [Provision web servers] *******************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************
[WARNING]: Host 'devops-vm' is using the discovered Python interpreter at '/usr/bin/python3.12', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [devops-vm]

TASK [common : Update apt cache] ***************************************************************************************************************
ok: [devops-vm]

TASK [common : Install common packages] ********************************************************************************************************
changed: [devops-vm]

TASK [common : Set timezone to UTC] ************************************************************************************************************
ok: [devops-vm]

TASK [docker : Add Docker repo] ****************************************************************************************************************
changed: [devops-vm]

TASK [docker : update apt cache] ***************************************************************************************************************
changed: [devops-vm]

TASK [docker : Install Docker] *****************************************************************************************************************
changed: [devops-vm]

TASK [docker : Add ubuntu user to docker group] ************************************************************************************************
ok: [devops-vm]

RUNNING HANDLER [docker : restart docker] ******************************************************************************************************
changed: [devops-vm]

PLAY RECAP *************************************************************************************************************************************
devops-vm                  : ok=9    changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

```

### The next run

```text
timur@timur-ficus:~/proj/DevOps-Core-Course/ansible$ ansible-playbook playbooks/provision.yml

PLAY [Provision web servers] *******************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************
[WARNING]: Host 'devops-vm' is using the discovered Python interpreter at '/usr/bin/python3.12', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [devops-vm]

TASK [common : Update apt cache] ***************************************************************************************************************
ok: [devops-vm]

TASK [common : Install common packages] ********************************************************************************************************
ok: [devops-vm]

TASK [common : Set timezone to UTC] ************************************************************************************************************
ok: [devops-vm]

TASK [docker : Add Docker repo] ****************************************************************************************************************
ok: [devops-vm]

TASK [docker : update apt cache] ***************************************************************************************************************
skipping: [devops-vm]

TASK [docker : Install Docker] *****************************************************************************************************************
ok: [devops-vm]

TASK [docker : Add ubuntu user to docker group] ************************************************************************************************
ok: [devops-vm]

PLAY RECAP *************************************************************************************************************************************
devops-vm                  : ok=7    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
```

After this run, nothing changed. Even `apt update` was skipped because it is triggered by changes in `Add Docker repo`.

### Analysis: what changed the first time

Everything related to `apt` and `docker` because the packages were not installed.

### Why nothing changed the second time

This is why we need Ansible: it checks that the system is in the desired state before doing anything (providing
idempotency). The system was already in the desired state because Ansible was run just before.


# Task 3

### Terminal output

```text
timur@timur-ficus:~/proj/DevOps-Core-Course/ansible$ ansible-playbook playbooks/deploy.yml --ask-vault-pass
Vault password: 

PLAY [Deploy application] **********************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************
[WARNING]: Host 'devops-vm' is using the discovered Python interpreter at '/usr/bin/python3.12', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [devops-vm]

TASK [app_deploy : load vault] *****************************************************************************************************************
ok: [devops-vm]

TASK [app_deploy : DockerHub Login] ************************************************************************************************************
changed: [devops-vm]

TASK [app_deploy : Pull image] *****************************************************************************************************************
changed: [devops-vm]

TASK [app_deploy : Stop and remove running container] ******************************************************************************************
ok: [devops-vm]

TASK [app_deploy : Run container] **************************************************************************************************************
changed: [devops-vm]

TASK [app_deploy : Wait for port] **************************************************************************************************************
ok: [devops-vm]

TASK [app_deploy : Healthcheck] ****************************************************************************************************************
ok: [devops-vm]

PLAY RECAP *************************************************************************************************************************************
devops-vm                  : ok=8    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

### `docker ps` output

```text
vboxuser@devops-vm:~$ docker ps
CONTAINER ID   IMAGE                                    COMMAND                  CREATED              STATUS              PORTS                    NAMES
0cdb6ce0a0f5   timurusmanov/devops-infoservice:latest   "gunicorn -b 0.0.0.0…"   About a minute ago   Up About a minute   0.0.0.0:5000->5000/tcp   devops-infoservice
```

### Healthcheck

Healthcheck passed: Ansible printed `ok`.

# Task 4

## Architecture overview

## 1. Architecture Overview
### Ansible version used
```text
ansible [core 2.20.2]
  config file = None
  configured module search path = ['/home/timur/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3.14/site-packages/ansible
  ansible collection location = /home/timur/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/bin/ansible
  python version = 3.14.3 (main, Feb 13 2026, 15:31:44) [GCC 15.2.1 20260209] (/usr/bin/python)
  jinja version = 3.1.6
  pyyaml version = 6.0.3 (with libyaml v0.2.5)
```

### Target VM OS and version
Ubuntu 24.04 LTS

### Role structure diagram or explanation
3 roles:
1. `common` for setting up necessary system software and configuration
2. `docker` for installing Docker
3. `app_deploy` for pulling and running the application.

### Why roles instead of monolithic playbooks?
Roles act as reusable and invokable playbooks. Increases modularity.

## 2. Roles Documentation

### common
- **Purpose**: Configure the system and set up common software.
- **Variables**: `common_packages` contains a list of packages to install
- **Handlers**: none
- **Dependencies**: no other roles needed

### docker
- **Purpose**: Install the latest Docker version and configure the system
- **Variables**: `ubuntu_user` is the user to add to the `docker` group, in my case `vboxuser`
- **Handlers**: `restart docker` restarts the daemon
- **Dependencies**: no other roles required

### app\_deploy
- **Purpose**: Pull and run the app
- **Variables in the role**:
    - `default_port: 5000` is the listened port inside the container
    - `default_restart_policy: unless-stopped`
    - `default_environment_variables: '{}'` is the env. variables passed to the app
- **Variables in the vault** `group_vars/all.yml`:
    - `dockerhub_username` is my username on DockerHub
    - `dockerhub_password` is my PAT (by principle of least privilege, it grants read-only access only to public images)
    - `app_name: devops-infoservice` is the container and image name (without my username)
    - `docker_image: "{{ dockerhub_username }}/{{ app_name }}"` is the full image name on DockerHub
    - `docker_image_tag: latest`, as required by the lab
    - `app_port: 5000` is the port exposed on the VM
    - `app_container_name: "{{ app_name }}"` is the container name
- **Handlers**: `restart container` restarts the container
- **Dependencies**: requires the `docker` role to run before it

## 3. Idempotency Demonstration
### Terminal output from FIRST provision.yml run
See Task 2.
### Terminal output from SECOND provision.yml run
See Task 2.
### Analysis: What changed first time? What didn't change second time?
See Task 2.
### Explanation: What makes your roles idempotent?
I took care to specify the desired state of the machine instead of imperatively running the commands.
This way, Ansible can determine what it actually needs to run, and, of course, on the second run there will be nothing
to do.

## 4. Ansible Vault Usage
### How you store credentials securely
I store them in the `group_vars/all.yml` vault (encrypted with a password).
### Vault password management strategy
The password is stored securely inside my head ;)
So unless you apply a soldering iron directly to the head, you will not extract it.
### Example of encrypted file (show it's encrypted!)
For example:
```sh
head -n 2 group_vars/all.yml
```
Yields:
```text
$ANSIBLE_VAULT;1.1;AES256
35666430376135623761373732656538383137656466336266366239303435363364353462323136
```
So this file is an unreadable Ansible vault that uses AES256 symmetric encryption.

### Why Ansible Vault is important
Since I have to push the variable file to GitHub, I have to encrypt it so that nobody can see the credentials.

## 5. Deployment Verification
See Task 3.

## 6. Key Decisions
### Why use roles instead of plain playbooks?
See **Why roles instead of monolithic playbooks?** in **Architecture overview**.
### How do roles improve reusability?
When done correctly, a role acts like a module that does one specific task and does it well.
This allows engineers to paste the same role into new projects.

### What makes a task idempotent?
When the task specifies what the system should be like by the end of the task, it can be re-run multiple times, but
runs after the first one will see that the system is already in the desired state and do nothing.

### How do handlers improve efficiency?
Handlers only execute when a task has changed the system state, not always. That reduces overhead.

### Why is Ansible Vault necessary?
See **Why Ansible Vault is important** in **Ansible Vault Usage**.

## 7. Challenges (Optional)
### Issues encountered and solutions
- Running `apt update` only if the docker repo has been newly added. Tried handlers, but it turned out they only run
  after all tasks have run (which really should have been clarified better in the lecture, IMHO).

