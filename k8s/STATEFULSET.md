# StatefulSet Overview

**StatefulSet Use Cases:**
- Databases (MySQL, PostgreSQL, MongoDB)
- Message queues (Kafka, RabbitMQ)
- Distributed systems (Elasticsearch, Cassandra)

**Key Differences:**

| Feature | Deployment | StatefulSet |
|---------|------------|-------------|
| Pod Names | Random suffix | Ordered index (pod-0, pod-1) |
| Storage | Shared PVC | Per-pod PVC via templates |
| Scaling | Any order | Ordered (0→1→2) |
| Network ID | Random | Stable DNS name |

**Headless Service:**
A Service with `clusterIP: None` creates DNS records for each pod:
- `pod-0.service-name.namespace.svc.cluster.local`

# Resource Verification

```bash
kubectl get statefulset
```
```text
NAME         READY   AGE
dinfochart   5/5     3m23s
```
```bash
kubectl get pods
```
```text
NAME           READY   STATUS    RESTARTS   AGE
dinfochart-0   1/1     Running   0          3m31s
dinfochart-1   1/1     Running   0          3m23s
dinfochart-2   1/1     Running   0          3m17s
dinfochart-3   1/1     Running   0          3m11s
dinfochart-4   1/1     Running   0          3m6s
```
```bash
kubectl get pvc
```
```text
NAME                           STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
data-dinfochart-0              Bound    pvc-784ff82c-411e-4a10-b051-7c83c2cb4b97   100Mi      RWO            standard       <unset>                 10m
dinfochart-data                Bound    pvc-70bb3538-0219-4095-b89d-9b660b8e7b57   100Mi      RWO            standard       <unset>                 3m38s
dinfochart-data-dinfochart-0   Bound    pvc-e23d9b83-fdfa-4aee-a16b-0d9c88f3b280   100Mi      RWO            standard       <unset>                 3m38s
dinfochart-data-dinfochart-1   Bound    pvc-567e3999-61c7-4296-b1ba-55cdcb738833   100Mi      RWO            standard       <unset>                 3m30s
dinfochart-data-dinfochart-2   Bound    pvc-b8897836-6f0e-4f1d-96bc-550579591d6d   100Mi      RWO            standard       <unset>                 3m24s
dinfochart-data-dinfochart-3   Bound    pvc-3c88cd06-04e5-4fbb-8099-779ab5523c84   100Mi      RWO            standard       <unset>                 3m18s
dinfochart-data-dinfochart-4   Bound    pvc-1d982389-ea92-4957-9e2d-450462809574   100Mi      RWO            standard       <unset>                 3m13s
```

# Network Identity

```text
/app # nslookup dinfochart-1.dinfochart-headless.default.svc.cluster.loc
al
Server:         10.96.0.10
Address:        10.96.0.10:53


Name:   dinfochart-1.dinfochart-headless.default.svc.cluster.local
Address: 10.244.0.10
```

# Per-Pod Storage Evidence
```text
timur@timur-ficus:~/proj/DevOps-Core-Course/k8s$ curl localhost:8080/vis
its
Handling connection for 8080
{"visits":1}
timur@timur-ficus:~/proj/DevOps-Core-Course/k8s$ curl localhost:8081/vis
its
Handling connection for 8081
{"visits":4}
```

# Persistence Test
```
timur@timur-ficus:~/proj/DevOps-Core-Course/k8s$ kubectl exec dinfochart
-0 -- cat /data/visits && echo
1
timur@timur-ficus:~/proj/DevOps-Core-Course/k8s$ kubectl delete pod dinf
ochart-0
pod "dinfochart-0" deleted from default namespace
timur@timur-ficus:~/proj/DevOps-Core-Course/k8s$ kubectl get pods
NAME           READY   STATUS    RESTARTS   AGE
dinfochart-0   1/1     Running   0          10s
dinfochart-1   1/1     Running   0          20m
dinfochart-2   1/1     Running   0          19m
dinfochart-3   1/1     Running   0          19m
dinfochart-4   1/1     Running   0          19m
timur@timur-ficus:~/proj/DevOps-Core-Course/k8s$ kubectl exec dinfochart
-0 -- cat /data/visits && echo
1
```
