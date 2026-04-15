# Chart Overview
### Chart structure explanation
Here is the file tree structure:

```
dinfochart/
├── charts
├── Chart.yaml
├── templates
│   ├── deployment.yaml
│   ├── _helpers.tpl
│   ├── hooks
│   │   ├── post-install-job.yaml
│   │   └── pre-install-job.yaml
│   ├── NOTES.txt
│   └── service.yaml
├── values-dev.yaml
├── values-prod.yaml
└── values.yaml
```

### Key template files and their purpose
- `_helpers.tpl`: defines helpful values for templates
- `deployment.yaml`: defines the structure for the k8s deployment
- `service.yaml`: defines the structure for the k8s service

### Values organization strategy
We extract the values or blocks that we would like to be configurable from the `.yaml` files into `values.yaml`,
preserving the original names for clarity.

# Configuration Guide
### Important values and their purpose

- `replicaCount`: number of pods that will be run.
- `image`: the information about which image to pull (name, tag)
- `service`: configuration for the reverse proxy
- `resources`: limits and reservations for memory and CPU time
- `livenessProbe`: command for checking the responsiveness of a container
- `readinessProbe`: command for checking the health of a container

### How to customize for different environments
We define another value file with overrides and later supply it in the command:

```bash
helm install myapp-dev k8s/mychart -f k8s/mychart/values-dev.yaml
```

Or specify overrides right in the command line:
```bash
helm install myapp k8s/mychart --set replicaCount=10
```

### Example installations with different configurations
As shown in the lab material:
```bash
# Development
helm install myapp-dev k8s/mychart -f k8s/mychart/values-dev.yaml

# Production
helm install myapp-prod k8s/mychart -f k8s/mychart/values-prod.yaml

# Override specific value
helm install myapp k8s/mychart --set replicaCount=10
```

# Hook Implementation
### What hooks you implemented and why
I implemented the pre-install hook and the post-install one. I did that because it was prescribed by the lab.

### Hook execution order and weights
Hook         | Order  | Weight
------------------------------
Pre-install  | Before | -5
Post-install | After  | 5

### Deletion policies explanation
It allows to set a rule that dictates when the executed hook jobs will be deleted. `before-hook-creation` means right
before the hook is run, its previous invokation will be deleted. `hook-succeeded` and `hook-failed` delete the hook
immediately after it succeeds or fails (respectively).

# Installation Evidence
### `helm list` output
```text
NAME     	NAMESPACE	REVISION	UPDATED                               	STATUS  	CHART           	APP VERSION
myrelease	default  	1       	2026-04-02 18:01:48.36966193 +0300 MSK	deployed	dinfochart-0.1.0	1.1.1      
```

### `kubectl get all` showing deployed resources
```text
NAME                                        READY   STATUS    RESTARTS   AGE
pod/myrelease-dinfochart-5b67fb98d9-2jk9d   1/1     Running   0          22m
pod/myrelease-dinfochart-5b67fb98d9-8c448   1/1     Running   0          22m
pod/myrelease-dinfochart-5b67fb98d9-fq5mz   1/1     Running   0          22m
pod/myrelease-dinfochart-5b67fb98d9-v5zjk   1/1     Running   0          22m
pod/myrelease-dinfochart-5b67fb98d9-wtx52   1/1     Running   0          22m

NAME                           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/kubernetes             ClusterIP   10.96.0.1       <none>        443/TCP        9d
service/myrelease-dinfochart   NodePort    10.102.118.72   <none>        80:30952/TCP   22m

NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/myrelease-dinfochart   5/5     5            5           22m

NAME                                              DESIRED   CURRENT   READY   AGE
replicaset.apps/myrelease-dinfochart-5b67fb98d9   5         5         5       22m
```
### Hook execution output (`kubectl get jobs`, `kubectl describe job`)
As per the deletion policy, the hook jobs get deleted after they run and succeed, which is my case. These commands
report errors because there are no jobs to inspect.

### Different environment deployments (dev vs prod)
`dev` is for testing the latest changes (with the `latest` tag, plenty of resources).

`prod` is for deployment on a real cluster (with a fixed version and limited resources).

# Operations
### Installation commands used
```text
helm install <name> <what to install> [-f <value overrides>]
```

### How to upgrade a release
```bash
helm upgrade myrelease ./mychart
```

### How to rollback
```bash
helm rollback myrelease 1
```

### How to uninstall
```bash
helm uninstall myrelease
```

# Testing & Validation
### `helm lint` output
```text
==> Linting dinfochart/
[INFO] Chart.yaml: icon is recommended

1 chart(s) linted, 0 chart(s) failed
```

### `helm template` verification
```yaml
---
# Source: dinfochart/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: release-name-dinfochart
  labels:
    helm.sh/chart: dinfochart-0.1.0
    app.kubernetes.io/name: dinfochart
    app.kubernetes.io/instance: release-name
    app.kubernetes.io/version: "1.1.1"
    app.kubernetes.io/managed-by: Helm
spec:
  type: NodePort
  selector:
    app.kubernetes.io/name: dinfochart
    app.kubernetes.io/instance: release-name
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
---
# Source: dinfochart/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: release-name-dinfochart
  labels:
    helm.sh/chart: dinfochart-0.1.0
    app.kubernetes.io/name: dinfochart
    app.kubernetes.io/instance: release-name
    app.kubernetes.io/version: "1.1.1"
    app.kubernetes.io/managed-by: Helm
spec:
  replicas: 5
  selector:
    matchLabels:
      app.kubernetes.io/name: dinfochart
      app.kubernetes.io/instance: release-name
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Extra pods during update
      maxUnavailable: 0  # Ensure availability
  template:
    metadata:
      labels:
        helm.sh/chart: dinfochart-0.1.0
        app.kubernetes.io/name: dinfochart
        app.kubernetes.io/instance: release-name
        app.kubernetes.io/version: "1.1.1"
        app.kubernetes.io/managed-by: Helm
    spec:
      containers:
        - name: dinfochart
          image:  "timurusmanov/devops-infoservice:1.1.1"
          ports:
          - containerPort: 80
          resources:
            limits:
              cpu: 200m
              memory: 256Mi
            requests:
              cpu: 100m
              memory: 128Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 10
            periodSeconds: 5
          readinessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 5
            periodSeconds: 3
---
# Source: dinfochart/templates/hooks/post-install-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: 'release-name-dinfochart-post-install'
  labels:
    helm.sh/chart: dinfochart-0.1.0
    app.kubernetes.io/name: dinfochart
    app.kubernetes.io/instance: release-name
    app.kubernetes.io/version: "1.1.1"
    app.kubernetes.io/managed-by: Helm
  annotations:
    "helm.sh/hook": post-install
    "helm.sh/hook-weight": "5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    metadata:
      name: 'release-name-dinfochart-post-install'
    spec:
      restartPolicy: Never
      containers:
      - name: post-install-job
        image: busybox
        command: ['sh', '-c', 'echo Post-install validation && sleep 1 && echo Validation passed']
---
# Source: dinfochart/templates/hooks/pre-install-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: 'release-name-dinfochart-pre-install'
  labels:
    helm.sh/chart: dinfochart-0.1.0
    app.kubernetes.io/name: dinfochart
    app.kubernetes.io/instance: release-name
    app.kubernetes.io/version: "1.1.1"
    app.kubernetes.io/managed-by: Helm
  annotations:
    "helm.sh/hook": pre-install
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    metadata:
      name: 'release-name-dinfochart-pre-install'
    spec:
      restartPolicy: Never
      containers:
      - name: pre-install-job
        image: busybox
        command: ['sh', '-c', 'echo Pre-install task running && sleep 1 && echo Pre-install completed']
```

### Dry-run output
```yaml
NAME: test-release
LAST DEPLOYED: Thu Apr  2 18:29:57 2026
NAMESPACE: default
STATUS: pending-install
REVISION: 1
DESCRIPTION: Dry run complete
TEST SUITE: None
HOOKS:
---
# Source: dinfochart/templates/hooks/post-install-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: 'test-release-dinfochart-post-install'
  labels:
    helm.sh/chart: dinfochart-0.1.0
    app.kubernetes.io/name: dinfochart
    app.kubernetes.io/instance: test-release
    app.kubernetes.io/version: "1.1.1"
    app.kubernetes.io/managed-by: Helm
  annotations:
    "helm.sh/hook": post-install
    "helm.sh/hook-weight": "5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    metadata:
      name: 'test-release-dinfochart-post-install'
    spec:
      restartPolicy: Never
      containers:
      - name: post-install-job
        image: busybox
        command: ['sh', '-c', 'echo Post-install validation && sleep 1 && echo Validation passed']
---
# Source: dinfochart/templates/hooks/pre-install-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: 'test-release-dinfochart-pre-install'
  labels:
    helm.sh/chart: dinfochart-0.1.0
    app.kubernetes.io/name: dinfochart
    app.kubernetes.io/instance: test-release
    app.kubernetes.io/version: "1.1.1"
    app.kubernetes.io/managed-by: Helm
  annotations:
    "helm.sh/hook": pre-install
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    metadata:
      name: 'test-release-dinfochart-pre-install'
    spec:
      restartPolicy: Never
      containers:
      - name: pre-install-job
        image: busybox
        command: ['sh', '-c', 'echo Pre-install task running && sleep 1 && echo Pre-install completed']
MANIFEST:
---
# Source: dinfochart/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: test-release-dinfochart
  labels:
    helm.sh/chart: dinfochart-0.1.0
    app.kubernetes.io/name: dinfochart
    app.kubernetes.io/instance: test-release
    app.kubernetes.io/version: "1.1.1"
    app.kubernetes.io/managed-by: Helm
spec:
  type: NodePort
  selector:
    app.kubernetes.io/name: dinfochart
    app.kubernetes.io/instance: test-release
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
---
# Source: dinfochart/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-release-dinfochart
  labels:
    helm.sh/chart: dinfochart-0.1.0
    app.kubernetes.io/name: dinfochart
    app.kubernetes.io/instance: test-release
    app.kubernetes.io/version: "1.1.1"
    app.kubernetes.io/managed-by: Helm
spec:
  replicas: 5
  selector:
    matchLabels:
      app.kubernetes.io/name: dinfochart
      app.kubernetes.io/instance: test-release
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Extra pods during update
      maxUnavailable: 0  # Ensure availability
  template:
    metadata:
      labels:
        helm.sh/chart: dinfochart-0.1.0
        app.kubernetes.io/name: dinfochart
        app.kubernetes.io/instance: test-release
        app.kubernetes.io/version: "1.1.1"
        app.kubernetes.io/managed-by: Helm
    spec:
      containers:
        - name: dinfochart
          image:  "timurusmanov/devops-infoservice:1.1.1"
          ports:
          - containerPort: 80
          resources:
            limits:
              cpu: 200m
              memory: 256Mi
            requests:
              cpu: 100m
              memory: 128Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 10
            periodSeconds: 5
          readinessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 5
            periodSeconds: 3
```

### Application accessibility verification
```bash
kubectl port-forward service/myrelease-dinfochart 8080:80 &
curl localhost:8080/health
```
```json
{"status":"healthy","timestamp":"2026-04-02T15:35:47.354190+00:00","uptime_seconds":2010}
```
