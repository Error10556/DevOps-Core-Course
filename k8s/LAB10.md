# Task 1

### Installation
```sh
sudo pacman -S --needed helm
```
```text
warning: helm-4.1.3-1 is up to date -- skipping
 there is nothing to do
```

### Version
```sh
helm version
```
```text
version.BuildInfo{Version:"v4.1.3", GitCommit:"c94d381b03be117e7e57908edbf642104e00eb8f", GitTreeState:"", GoVersion:"go1.26.1-X:nodwarf5", KubeClientVersion:"v1.35"}
```

### Output of exploring a public chart

```sh
helm show chart prometheus-community/prometheus
```
```yaml
annotations:
  artifacthub.io/license: Apache-2.0
  artifacthub.io/links: |
    - name: Chart Source
      url: https://github.com/prometheus-community/helm-charts
    - name: Upstream Project
      url: https://github.com/prometheus/prometheus
apiVersion: v2
appVersion: v3.10.0
dependencies:
- condition: alertmanager.enabled
  name: alertmanager
  repository: https://prometheus-community.github.io/helm-charts
  version: 1.34.*
- condition: kube-state-metrics.enabled
  name: kube-state-metrics
  repository: https://prometheus-community.github.io/helm-charts
  version: 7.2.*
- condition: prometheus-node-exporter.enabled
  name: prometheus-node-exporter
  repository: https://prometheus-community.github.io/helm-charts
  version: 4.52.*
- condition: prometheus-pushgateway.enabled
  name: prometheus-pushgateway
  repository: https://prometheus-community.github.io/helm-charts
  version: 3.6.*
description: Prometheus is a monitoring system and time series database.
home: https://prometheus.io/
icon: https://raw.githubusercontent.com/prometheus/prometheus.github.io/master/assets/prometheus_logo-cb55bb5c346.png
keywords:
- monitoring
- prometheus
kubeVersion: '>=1.19.0-0'
maintainers:
- email: gianrubio@gmail.com
  name: gianrubio
  url: https://github.com/gianrubio
- email: zanhsieh@gmail.com
  name: zanhsieh
  url: https://github.com/zanhsieh
- email: miroslav.hadzhiev@gmail.com
  name: Xtigyro
  url: https://github.com/Xtigyro
- email: naseem@transit.app
  name: naseemkullah
  url: https://github.com/naseemkullah
- email: rootsandtrees@posteo.de
  name: zeritti
  url: https://github.com/zeritti
name: prometheus
sources:
- https://github.com/prometheus/alertmanager
- https://github.com/prometheus/prometheus
- https://github.com/prometheus/pushgateway
- https://github.com/prometheus/node_exporter
- https://github.com/kubernetes/kube-state-metrics
type: application
version: 28.14.1
```

# Task 2

```sh
helm lint dinfochart
```
```text
==> Linting dinfochart
[INFO] Chart.yaml: icon is recommended

1 chart(s) linted, 0 chart(s) failed
```

```sh
helm template dinfochart dinfochart/
```
```yaml
---
# Source: dinfochart/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: dinfochart
  labels:
    helm.sh/chart: dinfochart-0.1.0
    app.kubernetes.io/name: dinfochart
    app.kubernetes.io/instance: dinfochart
    app.kubernetes.io/version: "1.1.1"
    app.kubernetes.io/managed-by: Helm
spec:
  type: NodePort
  selector:
    app.kubernetes.io/name: dinfochart
    app.kubernetes.io/instance: dinfochart
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
---
# Source: dinfochart/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dinfochart
  labels:
    helm.sh/chart: dinfochart-0.1.0
    app.kubernetes.io/name: dinfochart
    app.kubernetes.io/instance: dinfochart
    app.kubernetes.io/version: "1.1.1"
    app.kubernetes.io/managed-by: Helm
spec:
  replicas: 5
  selector:
    matchLabels:
      app.kubernetes.io/name: dinfochart
      app.kubernetes.io/instance: dinfochart
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
        app.kubernetes.io/instance: dinfochart
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

```sh
helm install --dry-run --debug test-release dinfochart/
```
```text
level=WARN msg="--dry-run is deprecated and should be replaced with '--dry-run=client'"
level=DEBUG msg="Original chart version" version=""
level=DEBUG msg="Chart path" path=/home/timur/proj/DevOps-Core-Course/k8s/dinfochart
level=DEBUG msg="number of dependencies in the chart" chart=dinfochart dependencies=0
NAME: test-release
LAST DEPLOYED: Thu Apr  2 17:17:49 2026
NAMESPACE: default
STATUS: pending-install
REVISION: 1
DESCRIPTION: Dry run complete
TEST SUITE: None
USER-SUPPLIED VALUES:
{}

COMPUTED VALUES:
image:
  pullPolicy: IfNotPresent
  repository: timurusmanov/devops-infoservice
  tag: 1.1.1
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
replicaCount: 5
resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi
service:
  port: 80
  targetPort: 5000
  type: NodePort

HOOKS:
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

```sh
helm install myrelease dinfochart/
```
```text
NAME: myrelease
LAST DEPLOYED: Thu Apr  2 17:18:20 2026
NAMESPACE: default
STATUS: deployed
REVISION: 1
DESCRIPTION: Install complete
TEST SUITE: None
```
