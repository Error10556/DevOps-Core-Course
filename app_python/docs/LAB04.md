# Lab 4

For this lab, I chose to use a local VM installation. I prefer that to using third-party services.

## Task 1

I elected to manually create a VM running Ubuntu 24 LTS with Oracle VirtualBox.

1. I downloaded the official Ubuntu 24.04 LTS image from [ubuntu.com](https://ubuntu.com/).
2. I configured the VM as shown in the screenshots below:

   ![Hardware](/app_python/docs/screenshots/Lab4-vhardware.png)

   ![Virtual disk](/app_python/docs/screenshots/Lab4-vdisk.png)

3. I ran the **unattended installation**. It reported an error at the end, but upon reboot, the system was installed
   correctly.

   ![Login screen](/app_python/docs/screenshots/Lab4-loginscreen.png)

4. Then I configured a shared folder to share my SSH key from the host machine to the guest one.

   ![Shared folder options window](/app_python/docs/screenshots/Lab4-sharedfolder.png)

5. I configured port forwarding from host:`10022` to guest:`22`.

   ![Port forwarding window](/app_python/docs/screenshots/Lab4-portforward.png)

6. Finally, I installed `ssh` on the guest VM and added my public key to `~/.ssh/authorized_keys`.

```sh
cat ~/Desktop/fwd/mypubkey >> ~/.ssh/authorized_keys
```
   No need to manage permissions, they were OK when I installed SSH.

   I could login to the VM with `ssh -p 10022 vboxuser@localhost`:

   ![SSH](/app_python/docs/screenshots/Lab4-sshlogin.png)


## Task 3

#### Setup documentation

- **Virtualization software**: Oracle VirtualBox 7.2.6
- **Guest OS**: Ubuntu 24.04 LTS
- **Virtual Hardware**:

| **Property**  | **Value** |
| ---           | ---       |
| Storage space | 24 GB     |
| RAM Volume    | 4 GB      |
| CPU Cores     | 4         |

- **Port forwarding**:

| **Host Address** | **Guest Address** |
| ---              | ---               |
| 127.0.0.1:10022  | 0.0.0.0:22        |

- **Guest Software**: OpenSSH 9.6p1 Ubuntu-3ubuntu13.14, OpenSSL 3.0.13 30 Jan 2024
