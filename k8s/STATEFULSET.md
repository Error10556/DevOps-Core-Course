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

# Network Identity
# Per-Pod Storage Evidence
# Persistence Test

1. **StatefulSet Overview** - Why StatefulSet, differences from Deployment
2. **Resource Verification** - Output of `kubectl get po,sts,svc,pvc`
3. **Network Identity** - DNS resolution outputs
4. **Per-Pod Storage Evidence** - Different visit counts per pod
5. **Persistence Test** - Data survives pod deletion
