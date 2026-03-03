# Task 1

```sh
# Test provision with only docker
ansible-playbook playbooks/provision.yml --tags "docker" --ask-vault-pass
```

```text
PLAY [Provision web servers] ***************************************************

TASK [Gathering Facts] *********************************************************
ok: [devops-vm]

TASK [docker : Add Docker repo] ************************************************
ok: [devops-vm]

TASK [docker : update apt cache] ***********************************************
skipping: [devops-vm]

TASK [docker : Install Docker] *************************************************
ok: [devops-vm]

TASK [docker : Ensure Docker is running] ***************************************
ok: [devops-vm]

TASK [docker : Add ubuntu user to docker group] ********************************
ok: [devops-vm]

PLAY RECAP *********************************************************************
devops-vm                  : ok=5    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
```

```sh
# Skip common role
ansible-playbook playbooks/provision.yml --skip-tags "common" --ask-vault-pass
```

```text
PLAY [Provision web servers] ***************************************************

TASK [Gathering Facts] *********************************************************
ok: [devops-vm]

TASK [docker : Add Docker repo] ************************************************
ok: [devops-vm]

TASK [docker : update apt cache] ***********************************************
skipping: [devops-vm]

TASK [docker : Install Docker] *************************************************
ok: [devops-vm]

TASK [docker : Ensure Docker is running] ***************************************
ok: [devops-vm]

TASK [docker : Add ubuntu user to docker group] ********************************
ok: [devops-vm]

PLAY RECAP *********************************************************************
devops-vm                  : ok=5    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   

```

```sh
# Install packages only across all roles
ansible-playbook playbooks/provision.yml --tags "packages" --ask-vault-pass
```

```text
PLAY [Provision web servers] ***************************************************

TASK [Gathering Facts] *********************************************************
ok: [devops-vm]

TASK [common : Update apt cache] ***********************************************
ok: [devops-vm]

TASK [common : Install common packages] ****************************************
ok: [devops-vm]

TASK [common : Log completion] *************************************************
changed: [devops-vm]

PLAY RECAP *********************************************************************
devops-vm                  : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

```

```sh
# Check mode to see what would run
ansible-playbook playbooks/provision.yml --tags "docker" --check --ask-vault-pass
```

```text
PLAY [Provision web servers] ***************************************************

TASK [Gathering Facts] *********************************************************
ok: [devops-vm]

TASK [docker : Add Docker repo] ************************************************
ok: [devops-vm]

TASK [docker : update apt cache] ***********************************************
skipping: [devops-vm]

TASK [docker : Install Docker] *************************************************
ok: [devops-vm]

TASK [docker : Ensure Docker is running] ***************************************
ok: [devops-vm]

TASK [docker : Add ubuntu user to docker group] ********************************
ok: [devops-vm]

PLAY RECAP *********************************************************************
devops-vm                  : ok=5    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
```

```sh
# Run only docker installation tasks
ansible-playbook playbooks/provision.yml --tags "docker_install" --ask-vault-pass
```

```text
PLAY [Provision web servers] ***************************************************

TASK [Gathering Facts] *********************************************************
ok: [devops-vm]

TASK [docker : Add Docker repo] ************************************************
ok: [devops-vm]

TASK [docker : update apt cache] ***********************************************
skipping: [devops-vm]

TASK [docker : Install Docker] *************************************************
ok: [devops-vm]

TASK [docker : Ensure Docker is running] ***************************************
ok: [devops-vm]

PLAY RECAP *********************************************************************
devops-vm                  : ok=4    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
```

Note that in some invokations the "Log completion" task is always marked as "changed". This is the consequence of
logging `ansible-playbook` runs. The lab requires to log successful completion, so this is intentional.

**Tags:**

```sh
ansible-playbook playbooks/provision.yml --list-tags
```

```text
playbook: playbooks/provision.yml

  play #1 (webservers): Provision web servers	TAGS: []
      TASK TAGS: [common, docker, docker_config, docker_install, packages]
```

# Task 2

