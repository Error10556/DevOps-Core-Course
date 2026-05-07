## Argo Rollouts Setup
### Installation verification
```bash
kubectl argo rollouts version
```
```text
kubectl-argo-rollouts: v1.9.0+838d4e7
  BuildDate: 2026-03-20T21:08:11Z
  GitCommit: 838d4e792be666ec11bd0c80331e0c5511b5010e
  GitTreeState: clean
  GoVersion: go1.24.13
  Compiler: gc
  Platform: linux/amd64
```

### Dashboard access
![Dashboard](/k8s/screenshots/argo_rollout_dashboard.png)

## Canary Deployment
### Strategy configuration explained
The strategy gradually increases the weight of the new version (ratio). If I notice some issue, I have the chance to
abort the rollout.

### Step-by-step rollout progression (screenshots from dashboard)
![Steps](/k8s/screenshots/argo_rollout_steps.png)

Changed the tag to latest, paused at weight 20:

![20](/k8s/screenshots/argo_rollout_pause_20.png)

### Promotion and abort demonstration

Pressed abort:

![Abort](/k8s/screenshots/argo_rollout_aborted.png)

Pressing "Promote" would just eventually replace all pods with the "latest" pods.

## Blue-Green Deployment
### Strategy configuration explained
I added a new service with the "-preview" suffix (`roll-dinfochart-preview`). The strategy reflects that.

### Preview vs active service
They are identical in my configuration, but all are working.

### Promotion process
```bash
kubectl argo rollouts promote roll-dinfochart
```
```text
rollout 'roll-dinfochart' promoted
```

## Strategy Comparison
### When to use canary vs blue-green
Canary is useful when there are no resources to host twice as many containers, or it is fine to test the new version on
a subset of users in production.

Blue-green is useful when we need to launch a new version (tested) and switch the service to the new one with no
downtime because it immediately re-routes traffic to the new version.
