# Task 1

Terminal output:
```sh
kubectl cluster-info
```
```text
Kubernetes control plane is running at https://192.168.49.2:8443
CoreDNS is running at https://192.168.49.2:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

```sh
kubectl get nodes
```
```text
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   41m   v1.35.1
```
Explanation: I chose minikube as the de-facto default choice for local cluster setup.

# Task 2

```sh
kubectl describe deployment devops-infoservice
```
```text
Name:                   devops-infoservice
Namespace:              default
CreationTimestamp:      Tue, 24 Mar 2026 14:21:22 +0300
Labels:                 app=devops-infoservice
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=devops-infoservice
Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=devops-infoservice
  Containers:
   devops-infoservice:
    Image:      127.0.0.1:5000/timurusmanov/devops-infoservice:latest
    Port:       5000/TCP
    Host Port:  0/TCP
    Limits:
      cpu:     200m
      memory:  256Mi
    Requests:
      cpu:         100m
      memory:      128Mi
    Liveness:      http-get http://:5000/health delay=10s timeout=1s period=10s #success=1 #failure=3
    Readiness:     http-get http://:5000/health delay=5s timeout=1s period=10s #success=1 #failure=3
    Environment:   <none>
    Mounts:        <none>
  Volumes:         <none>
  Node-Selectors:  <none>
  Tolerations:     <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   devops-infoservice-684dd6c4d7 (3/3 replicas created)
Events:
  Type    Reason             Age    From                   Message
  ----    ------             ----   ----                   -------
  Normal  ScalingReplicaSet  6m38s  deployment-controller  Scaled up replica set devops-infoservice-684dd6c4d7 from 0 to 3
```

# Task 3

Verification:
```sh
kubectl get services
```
```text
NAME                         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
devops-infoservice-service   NodePort    10.106.40.29   <none>        80:30080/TCP   6m38s
kubernetes                   ClusterIP   10.96.0.1      <none>        443/TCP        146m
```
```sh
kubectl describe service devops-infoservice-service
```
```text
Name:                     devops-infoservice-service
Namespace:                default
Labels:                   <none>
Annotations:              <none>
Selector:                 app=devops-infoservice
Type:                     NodePort
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.106.40.29
IPs:                      10.106.40.29
Port:                     <unset>  80/TCP
TargetPort:               5000/TCP
NodePort:                 <unset>  30080/TCP
Endpoints:                10.244.0.46:5000,10.244.0.45:5000,10.244.0.44:5000
Session Affinity:         None
External Traffic Policy:  Cluster
Internal Traffic Policy:  Cluster
Events:                   <none>
```
```sh
kubectl get endpoints
```
```text
Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice
NAME                         ENDPOINTS                                            AGE
devops-infoservice-service   10.244.0.44:5000,10.244.0.45:5000,10.244.0.46:5000   6m50s
kubernetes                   192.168.49.2:8443                                    147m
```

# Task 4

## Scaling

```sh
kubectl apply -f k8s/deployment.yml
```
```text
deployment.apps/devops-infoservice configured
```
```sh
kubectl get pods
```
```text
NAME                                  READY   STATUS    RESTARTS   AGE
devops-infoservice-684dd6c4d7-2hnv5   1/1     Running   0          53s
devops-infoservice-684dd6c4d7-dbn8f   1/1     Running   0          53s
devops-infoservice-684dd6c4d7-h7sbd   1/1     Running   0          19m
devops-infoservice-684dd6c4d7-s645x   1/1     Running   0          19m
devops-infoservice-684dd6c4d7-w87mf   1/1     Running   0          19m
```

## Rolling updates

(Changed the tag to 1.0.0)

```sh
kubectl apply -f k8s/deployment.yml
```
```text
deployment.apps/devops-infoservice configured
```
```sh
kubectl rollout status deployment/devops-infoservice
```
```text
Waiting for deployment "devops-infoservice" rollout to finish: 1 out of 5 new replicas have been updated...
Waiting for deployment "devops-infoservice" rollout to finish: 1 out of 5 new replicas have been updated...
Waiting for deployment "devops-infoservice" rollout to finish: 1 out of 5 new replicas have been updated...
Waiting for deployment "devops-infoservice" rollout to finish: 2 out of 5 new replicas have been updated...
Waiting for deployment "devops-infoservice" rollout to finish: 2 out of 5 new replicas have been updated...
Waiting for deployment "devops-infoservice" rollout to finish: 2 out of 5 new replicas have been updated...
Waiting for deployment "devops-infoservice" rollout to finish: 2 out of 5 new replicas have been updated...
Waiting for deployment "devops-infoservice" rollout to finish: 3 out of 5 new replicas have been updated...
Waiting for deployment "devops-infoservice" rollout to finish: 3 out of 5 new replicas have been updated...
Waiting for deployment "devops-infoservice" rollout to finish: 3 out of 5 new replicas have been updated...
Waiting for deployment "devops-infoservice" rollout to finish: 3 out of 5 new replicas have been updated...
Waiting for deployment "devops-infoservice" rollout to finish: 4 out of 5 new replicas have been updated...
Waiting for deployment "devops-infoservice" rollout to finish: 4 out of 5 new replicas have been updated...
Waiting for deployment "devops-infoservice" rollout to finish: 4 out of 5 new replicas have been updated...
Waiting for deployment "devops-infoservice" rollout to finish: 4 out of 5 new replicas have been updated...
Waiting for deployment "devops-infoservice" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "devops-infoservice" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "devops-infoservice" rollout to finish: 1 old replicas are pending termination...
deployment "devops-infoservice" successfully rolled out
```
```sh
kubectl rollout history deployment/devops-infoservice
```
```text
deployment.apps/devops-infoservice 
REVISION  CHANGE-CAUSE
1         <none>
2         <none>
```
```sh
kubectl rollout undo deployment/devops-infoservice
```
```text
deployment.apps/devops-infoservice rolled back
```

# Task 5
See `k8s/README.md`
