# Stack Components
### Prometheus Operator
Simplifies Prometheus management

### Prometheus
Pulls metrics and allows querying them with PromQL

### Alertmanager
Sets up alerting

### Grafana
Displays metrics by Prometheus on a web UI

### kube-state-metrics
Provides metrics of Kubernetes pods

# Installation Evidence
```bash
kubectl get po,svc -n monitoring
```
```text
NAME                                                         READY   STATUS    RESTARTS   AGE
pod/alertmanager-monitoring-kube-prometheus-alertmanager-0   2/2     Running   0          10m
pod/monitoring-grafana-86c44d45cc-h8w2v                      3/3     Running   0          10m
pod/monitoring-kube-prometheus-operator-54f68d65b4-x6ldq     1/1     Running   0          10m
pod/monitoring-kube-state-metrics-5957bd45bc-9rt9l           1/1     Running   0          10m
pod/monitoring-prometheus-node-exporter-g7sn7                1/1     Running   0          10m
pod/prometheus-monitoring-kube-prometheus-prometheus-0       2/2     Running   0          10m

NAME                                              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
service/alertmanager-operated                     ClusterIP   None            <none>        9093/TCP,9094/TCP,9094/UDP   10m
service/monitoring-grafana                        ClusterIP   10.99.77.146    <none>        80/TCP                       10m
service/monitoring-kube-prometheus-alertmanager   ClusterIP   10.103.60.121   <none>        9093/TCP,8080/TCP            10m
service/monitoring-kube-prometheus-operator       ClusterIP   10.98.160.147   <none>        443/TCP                      10m
service/monitoring-kube-prometheus-prometheus     ClusterIP   10.96.72.173    <none>        9090/TCP,8080/TCP            10m
service/monitoring-kube-state-metrics             ClusterIP   10.110.127.71   <none>        8080/TCP                     10m
service/monitoring-prometheus-node-exporter       ClusterIP   10.96.201.21    <none>        9100/TCP                     10m
service/prometheus-operated                       ClusterIP   None            <none>        9090/TCP                     10m
```

# Dashboard Answers

### Pod Resources
![Pod Resources](/k8s/screenshots/monitoring_cpu_memory.png)

### Namespace Analysis
Since the prepared dashboards are BROKEN!!!, I did this with a custom query:
![Namespace Analysis](/k8s/screenshots/monitoring_cpu_namespace.png)

It shows that dinfochart-0 is uses 0.08 CPUs, while others use 0. That is because I run `curl` in a loop that requests
from dinfochart-0.

### Node Metrics
Again, queries by me:

![Node Metrics MB](/k8s/screenshots/monitoring_memory_MB.png)

(in MB)

![Node Metrics Percent](/k8s/screenshots/monitoring_memory_percent.png)

(in %)

### Kubelet
![Kubelet](/k8s/screenshots/monitoring_kubelet.png)

18 pods, 37 containers.

### Network
It seems that kubernetes does not provide traffic monitoring for headless services. At least I could not find the
metric.

### Alerts
![Kubelet](/k8s/screenshots/monitoring_alerts.png)

6 alerts.

# Init Containers

See directory `init-containers` for the K8s deployments. Very good deployments, the best really. See for yourself.
