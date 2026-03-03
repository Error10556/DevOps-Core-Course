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

The "docker" dependency is needed to ensure that the `web_app` role (that requires Docker to function) runs **after**
the `docker` role (which installs Docker).

First run:

```text
PLAY [Deploy application] ******************************************************

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

TASK [web_app : load vault] ****************************************************
ok: [devops-vm]

TASK [web_app : DockerHub Login] ***********************************************
ok: [devops-vm]

TASK [web_app : Create app directory] ******************************************
ok: [devops-vm]

TASK [web_app : Template docker-compose file] **********************************
changed: [devops-vm]

TASK [web_app : Deploy with docker-compose] ************************************
[WARNING]: Docker compose: unknown None: /opt/devops-infoservice/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion
changed: [devops-vm]

TASK [web_app : Wait for port] *************************************************
ok: [devops-vm]

TASK [web_app : Healthcheck] ***************************************************
ok: [devops-vm]

PLAY RECAP *********************************************************************
devops-vm                  : ok=12   changed=2    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
```
(2 changes)

Second run:
```text
PLAY [Deploy application] ******************************************************

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

TASK [web_app : load vault] ****************************************************
ok: [devops-vm]

TASK [web_app : DockerHub Login] ***********************************************
ok: [devops-vm]

TASK [web_app : Create app directory] ******************************************
ok: [devops-vm]

TASK [web_app : Template docker-compose file] **********************************
ok: [devops-vm]

TASK [web_app : Deploy with docker-compose] ************************************
[WARNING]: Docker compose: unknown None: /opt/devops-infoservice/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion
ok: [devops-vm]

TASK [web_app : Wait for port] *************************************************
ok: [devops-vm]

TASK [web_app : Healthcheck] ***************************************************
ok: [devops-vm]

PLAY RECAP *********************************************************************
devops-vm                  : ok=12   changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
```
(0 changes)

Evidence:
```sh
[timur@timur-croc ~/proj/DevOps-Core-Course/ansible]$ ssh vboxuser@127.0.0.1 -p 10022
```
```text
Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 6.17.0-14-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

Expanded Security Maintenance for Applications is not enabled.

13 updates can be applied immediately.
To see these additional updates run: apt list --upgradable

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status

Last login: Tue Mar  3 11:12:13 2026 from 10.0.2.2
```
```sh
vboxuser@devops-vm:~$ docker ps
```
```text
CONTAINER ID   IMAGE                                    COMMAND                  CREATED         STATUS         PORTS                    NAMES
eaa998499d91   timurusmanov/devops-infoservice:latest   "gunicorn -b 0.0.0.0…"   4 minutes ago   Up 4 minutes   0.0.0.0:5000->5000/tcp   devops-infoservice
```
```sh
vboxuser@devops-vm:~$ docker compose -f /opt/devops-infoservice/docker-compose.yml ps
```
```text
WARN[0000] /opt/devops-infoservice/docker-compose.yml: the attribute `version` is obsolete , it will be ignored, please remove it to avoid potential confusion 
NAME                 IMAGE                                    COMMAND                  SERVICE              CREATED         STATUS         PORTS
devops-infoservice   timurusmanov/devops-infoservice:latest   "gunicorn -b 0.0.0.0…"   devops-infoservice   4 minutes ago   Up 4 minutes   0.0.0.0:5000->5000/tcp
```
```sh
vboxuser@devops-vm:~$ curl http://localhost:5000
```
(output given as it appeared in the terminal)
```text
{"endpoints":[{"description":"Service information","method":"GET","path":"/"},{"descriptio
n":"Health check","method":"GET","path":"/health"}],"request":{"client_ip":"172.18.0.1","m
ethod":"GET","path":"/","user_agent":"curl/8.5.0"},"runtime":{"current_time":"2026-03-03T1
1:14:36.366+00:00","timezone":"UTC","uptime_human":"0 hours, 5 minutes","uptime_seconds":3
00},"service":{"description":"DevOps course info service","framework":"Flask","name":"devo
ps-info-service","version":"1.0.0"},"system":{"architecture":"x86_64","cpu_count":2,"hostn
ame":"eaa998499d91","platform":"Linux","platform_version":"#14~24.04.1-Ubuntu SMP PREEMPT_
DYNAMIC Thu Jan 15 15:52:10 UTC 2","python_version":"3.13.12"}}
vboxuser@devops-vm:~$ 
```

Contents of `docker-compose.yml`:
```text
version: '3.8'

services:
  devops-infoservice:
    image: timurusmanov/devops-infoservice:latest
    container_name: devops-infoservice
    ports:
      - 0.0.0.0:5000:5000
    environment: {}
    restart: unless-stopped
```

# Task 3

## Scenario 1

```sh
ansible-playbook playbooks/deploy.yml
```
```text
PLAY [Deploy application] ******************************************************

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

TASK [web_app : Include wipe tasks] ********************************************
included: /home/timur/proj/DevOps-Core-Course/ansible/roles/web_app/tasks/wipe.yml for devops-vm

TASK [web_app : Stop and remove containers] ************************************
skipping: [devops-vm]

TASK [web_app : Remove docker-compose file and directory] **********************
skipping: [devops-vm]

TASK [web_app : Log wipe completion] *******************************************
skipping: [devops-vm]

TASK [web_app : load vault] ****************************************************
ok: [devops-vm]

TASK [web_app : DockerHub Login] ***********************************************
ok: [devops-vm]

TASK [web_app : Create app directory] ******************************************
ok: [devops-vm]

TASK [web_app : Template docker-compose file] **********************************
ok: [devops-vm]

TASK [web_app : Deploy with docker-compose] ************************************
[WARNING]: Docker compose: unknown None: /opt/devops-infoservice/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion
ok: [devops-vm]

TASK [web_app : Wait for port] *************************************************
ok: [devops-vm]

TASK [web_app : Healthcheck] ***************************************************
ok: [devops-vm]

PLAY RECAP *********************************************************************
devops-vm                  : ok=13   changed=0    unreachable=0    failed=0    skipped=4    rescued=0    ignored=0   
```
All wiping tasks skipped, as expected.

```sh
ssh vboxuser@127.0.0.1 -p 10022 docker ps
```
```text
CONTAINER ID   IMAGE                                    COMMAND                  CREATED       STATUS       PORTS                    NAMES
eaa998499d91   timurusmanov/devops-infoservice:latest   "gunicorn -b 0.0.0.0…"   4 hours ago   Up 4 hours   0.0.0.0:5000->5000/tcp   devops-infoservice
```

## Scenario 2

```sh
ansible-playbook playbooks/deploy.yml \
  -e "web_app_wipe=true" \
  --tags web_app_wipe
```
```text
PLAY [Deploy application] ******************************************************

TASK [Gathering Facts] *********************************************************
ok: [devops-vm]

TASK [web_app : Load vault] ****************************************************
ok: [devops-vm]

TASK [web_app : Include wipe tasks] ********************************************
included: /home/timur/proj/DevOps-Core-Course/ansible/roles/web_app/tasks/wipe.yml for devops-vm

TASK [web_app : Stop and remove containers] ************************************
[WARNING]: Docker compose: unknown None: /opt/devops-infoservice/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion
changed: [devops-vm]

TASK [web_app : Remove docker-compose file and directory] **********************
changed: [devops-vm]

TASK [web_app : Log wipe completion] *******************************************
ok: [devops-vm] => {
    "msg": "Application devops-infoservice wiped successfully"
}

PLAY RECAP *********************************************************************
devops-vm                  : ok=6    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

```sh
ssh vboxuser@127.0.0.1 -p 10022 docker ps
```
```text
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```
```sh
ssh vboxuser@127.0.0.1 -p 10022 ls /opt
```
```text
containerd
VBoxGuestAdditions-7.2.6
```

## Scenario 3

```sh
ansible-playbook playbooks/deploy.yml -e "web_app_wipe=true"
```
```text
/usr/lib/python3.14/getpass.py:99: GetPassWarning: Can not control echo on the terminal.
  passwd = fallback_getpass(prompt, stream)
Warning: Password input may be echoed.
Vault password: 

PLAY [Deploy application] ******************************************************

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

TASK [web_app : Load vault] ****************************************************
ok: [devops-vm]

TASK [web_app : Include wipe tasks] ********************************************
included: /home/timur/proj/DevOps-Core-Course/ansible/roles/web_app/tasks/wipe.yml for devops-vm

TASK [web_app : load vault] ****************************************************
ok: [devops-vm]

TASK [web_app : Stop and remove containers] ************************************
[ERROR]: Task failed: Module failed: "/opt/devops-infoservice" is not a directory
Origin: /home/timur/proj/DevOps-Core-Course/ansible/roles/web_app/tasks/wipe.yml:6:7

4 - name: Wipe web application
5   block:
6     - name: Stop and remove containers
        ^ column 7

fatal: [devops-vm]: FAILED! => {"changed": false, "msg": "\"/opt/devops-infoservice\" is not a directory"}
...ignoring

TASK [web_app : Remove docker-compose file and directory] **********************
ok: [devops-vm]

TASK [web_app : Log wipe completion] *******************************************
ok: [devops-vm] => {
    "msg": "Application devops-infoservice wiped successfully"
}

TASK [web_app : DockerHub Login] ***********************************************
ok: [devops-vm]

TASK [web_app : Create app directory] ******************************************
changed: [devops-vm]

TASK [web_app : Template docker-compose file] **********************************
changed: [devops-vm]

TASK [web_app : Deploy with docker-compose] ************************************
[WARNING]: Docker compose: unknown None: /opt/devops-infoservice/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion
changed: [devops-vm]

TASK [web_app : Wait for port] *************************************************
ok: [devops-vm]

TASK [web_app : Healthcheck] ***************************************************
ok: [devops-vm]

PLAY RECAP *********************************************************************
devops-vm                  : ok=17   changed=3    unreachable=0    failed=0    skipped=1    rescued=0    ignored=1   
```
Here, the task of removing the containers failed because the project has been wiped previously, but this is fine, so the
error is ignored.

```sh
ssh vboxuser@127.0.0.1 -p 10022 "docker ps"
```
```text
CONTAINER ID   IMAGE                                    COMMAND                  CREATED         STATUS         PORTS                    NAMES
53b905e53d5c   timurusmanov/devops-infoservice:latest   "gunicorn -b 0.0.0.0…"   2 minutes ago   Up 2 minutes   0.0.0.0:5000->5000/tcp   devops-infoservice
```

# Scenario 4

```sh
# 4a: Tag specified but variable false (when condition blocks it)
ansible-playbook playbooks/deploy.yml --tags web_app_wipe
# Result: wipe tasks skipped, deployment runs normally
```
```text
PLAY [Deploy application] ******************************************************

TASK [Gathering Facts] *********************************************************
ok: [devops-vm]

TASK [web_app : Load vault] ****************************************************
ok: [devops-vm]

TASK [web_app : Include wipe tasks] ********************************************
included: /home/timur/proj/DevOps-Core-Course/ansible/roles/web_app/tasks/wipe.yml for devops-vm

TASK [web_app : Stop and remove containers] ************************************
skipping: [devops-vm]

TASK [web_app : Remove docker-compose file and directory] **********************
skipping: [devops-vm]

TASK [web_app : Log wipe completion] *******************************************
skipping: [devops-vm]

PLAY RECAP *********************************************************************
devops-vm                  : ok=3    changed=0    unreachable=0    failed=0    skipped=3    rescued=0    ignored=0   
```
Indeed, wiping was skipped.

```sh
# 4b: Variable true, deployment skipped (only wipe runs)
ansible-playbook playbooks/deploy.yml -e "web_app_wipe=true" --tags web_app_wipe
# Result: only wipe, no deployment
```
```text
PLAY [Deploy application] ******************************************************

TASK [Gathering Facts] *********************************************************
ok: [devops-vm]

TASK [web_app : Load vault] ****************************************************
ok: [devops-vm]

TASK [web_app : Include wipe tasks] ********************************************
included: /home/timur/proj/DevOps-Core-Course/ansible/roles/web_app/tasks/wipe.yml for devops-vm

TASK [web_app : Stop and remove containers] ************************************
[WARNING]: Docker compose: unknown None: /opt/devops-infoservice/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion
changed: [devops-vm]

TASK [web_app : Remove docker-compose file and directory] **********************
changed: [devops-vm]

TASK [web_app : Log wipe completion] *******************************************
ok: [devops-vm] => {
    "msg": "Application devops-infoservice wiped successfully"
}

PLAY RECAP *********************************************************************
devops-vm                  : ok=6    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
App wiped.

## Screenshot after clean install

![Browser in vm](/ansible/docs/LAB06_Screenshot_app_in_vm.png)

# Task 4

