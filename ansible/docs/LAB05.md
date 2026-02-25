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


## 2. Roles Documentation

For each role (common, docker, app_deploy):
### Purpose: What does this role do?
### Variables: Key variables and defaults
### Handlers: What handlers are defined?
### Dependencies: Does it depend on other roles?

## 3. Idempotency Demonstration
### Terminal output from FIRST provision.yml run
### Terminal output from SECOND provision.yml run
### Analysis: What changed first time? What didn't change second time?
### Explanation: What makes your roles idempotent?

## 4. Ansible Vault Usage
### How you store credentials securely
### Vault password management strategy
### Example of encrypted file (show it's encrypted!)
### Why Ansible Vault is important

## 5. Deployment Verification
### Terminal output from deploy.yml run
### Container status: `docker ps` output
### Health check verification: `curl` outputs
### Handler execution (if any)

## 6. Key Decisions
### Why use roles instead of plain playbooks?
### How do roles improve reusability?
### What makes a task idempotent?
### How do handlers improve efficiency?
### Why is Ansible Vault necessary?

## 7. Challenges (Optional)
### Issues encountered and solutions
### Keep it brief - bullet points OK


