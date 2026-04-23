## Application Changes
### Description of visits counter implementation
I created a class VisitCounter, instances of which read from `/data/visits` upon creation and support incrementing.
When incrementing, the object locks a `Lock`, increments the attribute, and saves the value to `/data/visits`.

The program creates one instance of `VisitCounter` and uses it in `GET /` (to increment) and `GET /visits` (to get the
current number of visits).

### New endpoint documentation
`GET /visits` returns an object of the format
```json
{
    "visits": 123
}
```

### Local testing evidence with Docker
I ran the new image with
```bash
docker run -it --rm -p 5000:5000 -e DEBUG=true -v ./data:/data timurusmanov/devops-infoservice:latest
```

Even after reloading, the number of visits does not reset:

```bash
cat data/visits
```
```text
5
```

## ConfigMap Implementation
### ConfigMap template structure
Apart from the common fields, it just defines `data:`.

### `config.json` content
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "dinfochart.fullname" . }}-config
data:
  config.json: |-
{{ .Files.Get "files/config.json" | indent 4 }}
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "dinfochart.fullname" . }}-env
data:
  APP_ENV: {{ .Values.environment | quote }}
  LOG_LEVEL: {{ .Values.logLevel | quote }}
```

### How ConfigMap is mounted as file
It is done with volume mounts in `deployment.yaml`:

```yaml
volumeMounts:
  - name: app-config
    mountPath: /config
    readOnly: true
```
...
```yaml
volumes:
  - name: app-config
    configMap:
      name: {{ include "dinfochart.fullname" . }}-config
```

### How ConfigMap provides environment variables
In the `envFrom` section, using `configMapRef`:
```yaml
envFrom:
  - configMapRef:
    name: {{ include "dinfochart.fullname" . }}-env
```

### Verification outputs
```bash
kubectl get pods
```
```text
NAME                         READY   STATUS    RESTARTS   AGE
dinfochart-54c9dd4c9-crjtl   1/1     Running   0          10m
```

```text
kubectl exec dinfochart-54c9dd4c9-crjtl -it -- sh
/app #
/app # env
KUBERNETES_PORT=tcp://10.96.0.1:443
KUBERNETES_SERVICE_PORT=443
LOG_LEVEL=
DINFOCHART_PORT_80_TCP=tcp://10.109.215.47:80
HOSTNAME=dinfochart-54c9dd4c9-crjtl
SHLVL=1
HOME=/root
GPG_KEY=7169605F62C751356D054A26A821E680E5FA6305
PYTHON_SHA256=2a84cd31dd8d8ea8aaff75de66fc1b4b0127dd5799aa50a64ae9a313885b4593
DINFOCHART_SERVICE_HOST=10.109.215.47
TERM=xterm
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
PATH=/venv/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
KUBERNETES_PORT_443_TCP_PORT=443
DINFOCHART_SERVICE_PORT=80
KUBERNETES_PORT_443_TCP_PROTO=tcp
DINFOCHART_PORT=tcp://10.109.215.47:80
PYTHON_VERSION=3.13.12
DINFOCHART_PORT_80_TCP_ADDR=10.109.215.47
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
KUBERNETES_SERVICE_PORT_HTTPS=443
DINFOCHART_PORT_80_TCP_PORT=80
VIRTUAL_ENV=/venv
APP_ENV=
DINFOCHART_PORT_80_TCP_PROTO=tcp
KUBERNETES_SERVICE_HOST=10.96.0.1
PWD=/app
/app #
/app # cat /config/config.json 
{
    "appname": "devops-infoservice",
    "environment": "prod",
}
```

## Persistent Volume
### PVC configuration explanation


### Access modes and storage class discussion
### Volume mount configuration
### Counter value before pod deletion
```bash
kubectl port-forward pods/dinfochart-667547c76b-n8m8j 8080:5000&
curl localhost:8080
curl localhost:8080
curl localhost:8080
curl localhost:8080
```
```bash
curl localhost:8080/visits
```
```text
4
```
### Pod deletion command
```bash
kubectl delete pod dinfochart-667547c76b-n8m8j
kubectl get pods
```
```text
NAME                          READY   STATUS    RESTARTS   AGE
dinfochart-667547c76b-p6w2c   1/1     Running   0          16s
```
(The pod restarted)
### Counter value after new pod starts
```bash
curl localhost:8080/visits
```
```text
4
```

## ConfigMap vs Secret
### When to use ConfigMap
ConfigMap is for providing non-sensitive configuration details.

### When to use Secret
`Secret` is for providing parameters whose value should not be seen by anybody.

## Required Screenshots/Outputs:

```bash
kubectl get configmap,pvc
```
```text
NAME                          DATA   AGE
configmap/dinfochart-config   1      30s
configmap/dinfochart-env      2      30s
configmap/kube-root-ca.crt    1      36m

NAME                                    STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
persistentvolumeclaim/dinfochart-data   Bound    pvc-11af931d-5ee4-4c4e-8364-cee981dc3183   100Mi      RWO            standard       <unset>                 30s
```
