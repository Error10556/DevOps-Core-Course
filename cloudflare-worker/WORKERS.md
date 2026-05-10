# Deployment Summary
### Worker URL
https://lab17.error10556.workers.dev

### Main routes
- `/` - the main endpoint, increments counter
- `/counter` - returns `{"count": <number of main page requests>}`
- `/health` - returns `{"status": "ok"}`
- `/edge` - returns information about the Cloudflare deployment used for this request

### Configuration used
I added the `APP_NAME` env. variable (`lab17`) and the `KV` key-value storage binding. This allows to keep the `count`
persistent.

# Evidence
### Screenshot of Cloudflare dashboard
![Dashboard](/cloudflare-worker/screenshots/dashboard.png)

### Example `/edge` JSON response
```bash
curl https://lab17.error10556.workers.dev/edge | jq
```
```json
{
  "colo": "ARN",
  "country": "FI",
  "city": "Helsinki",
  "asn": 56971,
  "httpProtocol": "HTTP/2",
  "tlsVersion": "TLSv1.3"
}
```
It shows a Finnish location because my proxy is located there.

### Example log or metrics screenshot
![Metrics](/cloudflare-worker/screenshots/metrics.png)

Logs in **Observability**:
![Logs](/cloudflare-worker/screenshots/logs.png)

# Kubernetes vs Cloudflare Workers Comparison

| Aspect | Kubernetes | Cloudflare Workers |
|--------|------------|--------------------|
| Setup complexity | Very difficult | Easy |
| Deployment speed | Depends on network & hardware | Fast |
| Global distribution | No | Automatic |
| Cost (for small apps) | Usually overpriced | Free |
| State/persistence model | Persistent Volume Claims, StatefulSets | KV storage |
| Control/flexibility | Great | Can be insufficient |
| Best use case | Large deployments | Small projects |

# When to Use Each
### Scenarios favoring Kubernetes
- Large deployments
- Powerful dedicated clusters
- Large professional teams
- Systems of containers

### Scenarios favoring Workers
- Need for global deployment
- TypeScript, JavaScript, Python projects
- Simple apps

### Your recommendation
If I had to choose between the two, I would go with Kubernetes.

Sure, Kubernetes is often overrated by system administrators. Many projects actually don't need that level of
complexity, and are better off deploying with docker-compose.

But still, Cloudflare workers are a bit too dependent on the Cloudflare infrastructure and ecosystem. This is especially
apparent in Russia.

So I choose digital freedom (k8s).

# Reflection
### What felt easier than Kubernetes?
Literally every step was easier for Workers, except maybe setting up `minikube`, which was very easy. No need to learn
arbitrary config schemas and package everything in containers.

### What felt more constrained?
Kubernetes gives more freedom in what kind of program we are actually running. K8s allows to deploy any container and
set them up in any way we need, whereas Workers makes you follow its project structure.

### What changed because Workers is not a Docker host?
Cannot deploy arbitrary containers.
