# Architecture Overview
## Diagram or description of your deployment architecture
I deploy 5 replicas of `devops-infoservice` to the `minikube` container. I use a kubernetes service as a load balancer.

## How many Pods, which Services, networking flow
There are 5 pods and 1 service that connects them with the "outside".

## Resource allocation strategy
We allocate 128MiB of space and 0.1CPU per Pod and allow at most 256MiB of space and 0.2CPU per Pod.

# Manifest Files
## Brief description of each manifest
`deployment.yml` provides information about the desired running containers.

`service.yml` provides information about the desired port forwarding configuration.

## Key configuration choices
Described in the lab requirements.

## Why you chose specific values (replicas, resources, etc.)
As required by the lab.

# Deployment Evidence
## `kubectl get all` output

```text
NAME                                      READY   STATUS    RESTARTS   AGE
pod/devops-infoservice-684dd6c4d7-69gqw   1/1     Running   0          11m
pod/devops-infoservice-684dd6c4d7-8zv2m   1/1     Running   0          10m
pod/devops-infoservice-684dd6c4d7-jr9mt   1/1     Running   0          10m
pod/devops-infoservice-684dd6c4d7-k4s5b   1/1     Running   0          11m
pod/devops-infoservice-684dd6c4d7-zg8cd   1/1     Running   0          10m

NAME                                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
service/devops-infoservice-service   NodePort    10.106.40.29   <none>        80:30080/TCP   29m
service/kubernetes                   ClusterIP   10.96.0.1      <none>        443/TCP        169m

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/devops-infoservice   5/5     5            5           39m

NAME                                            DESIRED   CURRENT   READY   AGE
replicaset.apps/devops-infoservice-5f7f6cb59c   0         0         0       14m
replicaset.apps/devops-infoservice-684dd6c4d7   5         5         5       39m
```

## `kubectl get pods,svc` with detailed view
```text
NAME                                      READY   STATUS    RESTARTS   AGE
pod/devops-infoservice-684dd6c4d7-69gqw   1/1     Running   0          11m
pod/devops-infoservice-684dd6c4d7-8zv2m   1/1     Running   0          11m
pod/devops-infoservice-684dd6c4d7-jr9mt   1/1     Running   0          11m
pod/devops-infoservice-684dd6c4d7-k4s5b   1/1     Running   0          11m
pod/devops-infoservice-684dd6c4d7-zg8cd   1/1     Running   0          10m

NAME                                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
service/devops-infoservice-service   NodePort    10.106.40.29   <none>        80:30080/TCP   29m
service/kubernetes                   ClusterIP   10.96.0.1      <none>        443/TCP        170m
```

## `kubectl describe deployment <name>` showing replicas and strategy
```text
Name:                   devops-infoservice
Namespace:              default
CreationTimestamp:      Tue, 24 Mar 2026 14:21:22 +0300
Labels:                 app=devops-infoservice
Annotations:            deployment.kubernetes.io/revision: 3
Selector:               app=devops-infoservice
Replicas:               5 desired | 5 updated | 5 total | 5 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  0 max unavailable, 1 max surge
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
OldReplicaSets:  devops-infoservice-5f7f6cb59c (0/0 replicas created)
NewReplicaSet:   devops-infoservice-684dd6c4d7 (5/5 replicas created)
Events:
  Type    Reason             Age                 From                   Message
  ----    ------             ----                ----                   -------
  Normal  ScalingReplicaSet  40m                 deployment-controller  Scaled up replica set devops-infoservice-684dd6c4d7 from 0 to 3
  Normal  ScalingReplicaSet  21m                 deployment-controller  Scaled up replica set devops-infoservice-684dd6c4d7 from 3 to 5
  Normal  ScalingReplicaSet  14m                 deployment-controller  Scaled up replica set devops-infoservice-5f7f6cb59c from 0 to 1
  Normal  ScalingReplicaSet  13m                 deployment-controller  Scaled down replica set devops-infoservice-684dd6c4d7 from 5 to 4
  Normal  ScalingReplicaSet  13m                 deployment-controller  Scaled up replica set devops-infoservice-5f7f6cb59c from 1 to 2
  Normal  ScalingReplicaSet  13m                 deployment-controller  Scaled down replica set devops-infoservice-684dd6c4d7 from 4 to 3
  Normal  ScalingReplicaSet  13m                 deployment-controller  Scaled up replica set devops-infoservice-5f7f6cb59c from 2 to 3
  Normal  ScalingReplicaSet  13m                 deployment-controller  Scaled down replica set devops-infoservice-684dd6c4d7 from 3 to 2
  Normal  ScalingReplicaSet  13m                 deployment-controller  Scaled up replica set devops-infoservice-5f7f6cb59c from 3 to 4
  Normal  ScalingReplicaSet  13m                 deployment-controller  Scaled down replica set devops-infoservice-684dd6c4d7 from 2 to 1
  Normal  ScalingReplicaSet  10m (x12 over 13m)  deployment-controller  (combined from similar events): Scaled down replica set devops-infoservice-5f7f6cb59c from 1 to 0
```

## Screenshot or curl output showing app working

![curl](/k8s/lab9-curl.png)

# Operations Performed
See `/labs/lab09.md`.

# Production Considerations
## What health checks did you implement and why?
I implemented the `/health` endpoint check to see if the container is healthy or some intervention is required.

## Resource limits rationale
As required by the lab.

## How would you improve this for production?
I would raise the resource limits and probably ditch `minikube`.

## Monitoring and observability strategy
Add `loki` + `grafana` + `prometheus` getting metrics from `/metrics`, but individually from every Pod.

# Challenges & Solutions
## Issues encountered
Docker's repositories are being blocked in Russia at the moment. I set up a local repo, put the images there, `exec`ed
into the `minikube` container and forwarded `localhost` to the host machine (which has the registry):
```sh
socat TCP4-LISTEN:5000,bind=127.0.0.1,fork TCP4:192.168.49.1:5000
```
