# ArgoCD Setup
### Installation verification
```bash
kubectl get pods --namespace argocd
```
```text
NAME                                                READY   STATUS    RESTARTS       AGE
argocd-application-controller-0                     1/1     Running   0              78m
argocd-applicationset-controller-559566846f-shch5   1/1     Running   0              78m
argocd-dex-server-8f5687997-8t499                   1/1     Running   0              78m
argocd-notifications-controller-56c7d65875-jbhv2    1/1     Running   0              78m
argocd-redis-fcd76bcfb-x97cm                        1/1     Running   0              78m
argocd-repo-server-7b8447858f-2vcj4                 1/1     Running   26 (10m ago)   78m
argocd-server-7f857f54f-m56tl                       1/1     Running   0              78m
```

### UI access method
![Argo UI](/k8s/screenshots/argo_ui.png)

### CLI configuration
![Argo UI](/k8s/screenshots/argo_cli_config.png)

# Application Configuration
### Application manifests
Complete listing:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: python-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/Error10556/DevOps-Core-Course.git
    targetRevision: lab13
    path: k8s/dinfochart
    helm:
      valueFiles:
        - values.yaml
        - values-dev.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
```

# Multi-Environment
### Dev vs Prod configuration differences
The only differences are shown below:

```diff
--- argocd/application-dev.yaml	2026-04-23 19:12:06.412196521 +0300
+++ argocd/application-prod.yaml	2026-04-23 19:25:09.577043976 +0300
@@ -12,13 +12,10 @@
     helm:
       valueFiles:
         - values.yaml
-        - values-dev.yaml
+        - values-prod.yaml
   destination:
     server: https://kubernetes.default.svc
-    namespace: dev
+    namespace: prod
   syncPolicy:
-    automated:
-      prune: true
-      selfHeal: true
     syncOptions:
       - CreateNamespace=true
```

### Sync policy differences and rationale
In production, automatic syncing may be dangerous. Syncing should be done manually when the team knows that the system
is stable (for example, if the staging environment rolled out fine).

### Namespace separation
The development version of the app deployment will be located in the `dev` namespace, and the production will be in the
`prod` namespace to ensure no collisions.

# Self-Healing Evidence
### Manual scale test with before/after
For example, assuming that the dev application is launched:
```bash
kubectl scale deployment devops-infoservice -n dev --replicas=2
```
After this, `argocd` automatically resets the replica count to 1.

### Pod deletion test
Kubernetes restarts deleted pods on its own, I think, but still:
```bash
kubectl delete pods/python-app-dinfochart-6d448c7957-cxjxj
```

This command just resets the alive time counter.

### Explanation of behaviors
ArgoCD automatically detects differences between the desired state and the real state of the deployment and can sync it
back to the desired state.

# Screenshots

See above.
