# Kubernetes Secrets
### Output of creating and viewing your secret
```sh
kubectl get secret app-credentials -o yaml
```
```text
apiVersion: v1
data:
  password: YWRtaW4xMjM=
  username: dGltdXI=
kind: Secret
metadata:
  creationTimestamp: "2026-04-08T14:10:34Z"
  name: app-credentials
  namespace: default
  resourceVersion: "7121"
  uid: cde19220-e95a-4b61-9386-b6b8f4b37f45
type: Opaque
```

### Decoded secret values demonstration
```sh
base64 -d <<<"dGltdXI="
```
```text
timur
```
```sh
base64 -d <<<"YWRtaW4xMjM="
```
```text
admin123
```

### Explanation of base64 encoding vs encryption
`base64`-encoding is is still plaintext: it obfuscates the information to a human reader, but the data is decodeable
with one command.

Real encryption requires the attacker to guess a key, which should be difficult to do.

# Helm Secret Integration
### Chart structure showing secrets.yaml
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-credentials
type: Opaque
stringData:
  username: {{ .Values.secret.username | quote }}
  password: {{ .Values.secret.password | quote }}
```

### How secrets are consumed in deployment
Secrets are consumed through environment variables.

### Verification output (env vars in pod, excluding actual values)
```sh
kubectl exec dinfoserv-dinfochart-575476d846-4424h -- env
```
```text
PATH=/venv/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=dinfoserv-dinfochart-575476d846-4424h
username=placeholder
password=placeholder
DINFOSERV_DINFOCHART_PORT_80_TCP=tcp://10.100.233.185:80
DINFOSERV_DINFOCHART_PORT_80_TCP_PROTO=tcp
KUBERNETES_PORT=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
DINFOSERV_DINFOCHART_PORT_80_TCP_PORT=80
KUBERNETES_SERVICE_HOST=10.96.0.1
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
DINFOSERV_DINFOCHART_SERVICE_HOST=10.100.233.185
DINFOSERV_DINFOCHART_SERVICE_PORT=80
DINFOSERV_DINFOCHART_PORT=tcp://10.100.233.185:80
DINFOSERV_DINFOCHART_PORT_80_TCP_ADDR=10.100.233.185
KUBERNETES_SERVICE_PORT=443
KUBERNETES_PORT_443_TCP_PROTO=tcp
GPG_KEY=7169605F62C751356D054A26A821E680E5FA6305
PYTHON_VERSION=3.13.12
PYTHON_SHA256=2a84cd31dd8d8ea8aaff75de66fc1b4b0127dd5799aa50a64ae9a313885b4593
VIRTUAL_ENV=/venv
HOME=/home/infoservice
```

Note the "username" and "password" env variables.

# Resource Management
### Resource limits configuration
Resource limits are configured with the `values` files.

### Explanation of requests vs limits
Requests = how much is guaranteed.
Limits = how much is the hard maximum.

### How to choose appropriate values
In the development environment, give more resources to debug and test.
In production, look at the cluster and see how much is available. Then assign that much as the limit. Requests are the
minimal requirements for the containers to function at all.

# Vault Integration
### Vault installation verification (`kubectl get pods`)
```text
NAME                                    READY   STATUS     RESTARTS   AGE
dinfoserv-dinfochart-b9cc59fdf-2dv4n    2/2     Running    0          4m4s
dinfoserv-dinfochart-b9cc59fdf-6chxr    2/2     Running    0          4m4s
dinfoserv-dinfochart-b9cc59fdf-b6cqg    2/2     Running    0          4m4s
dinfoserv-dinfochart-b9cc59fdf-fkfwn    2/2     Running    0          4m4s
dinfoserv-dinfochart-b9cc59fdf-nh9r2    2/2     Running    0          4m4s
vault-0                                 1/1     Running    0          15h
vault-agent-injector-848dd747d7-b2pt4   1/1     Running    0          15h
```

### Policy and role configuration (sanitized)
Policy:
```sh
cat >dinfoservice-secret-access.hcl <<EOF
path "secret/myapp/config" {
    capabilities = ["read"]
}
EOF
vault policy write dinfoservice-secret-access.hcl dinfoservice-secret-access.hcl
```

Role:
```sh
vault write auth/kubernetes/role/demo \
    bound_service_account_names=myapp \
    bound_service_account_namespaces=default \
    policies=default \
    ttl=1h
```

### Proof of secret injection (show file exists, path structure)
The secrets are mounted at `/etc/app-secret`:
```text
app-secret/
├── password
└── username
```

# Security Analysis
### Comparison: K8s Secrets vs Vault
K8s secrets are the native tool that is easy to use with kubernetes. HashiCorp Vault is a separate solution, although it
integrates well with Kubernetes.

K8s Secrets are stored in `etcd` by Kubernetes directly, by default unencrypted; Vault secrets are stored separately in
any provider that is configured, but that requires additional configuration.

### When to use each approach
There are ways to use both K8s secrets and HashiCorp Vault securely. But if the cloud provider, for example, provides a
secret management service, HC Vault probably will be easier to configure to use it, especially if the cloud provider
supplies documentation for that.
