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
### Sync policy differences and rationale
### Namespace separation

# Self-Healing Evidence
### Manual scale test with before/after
### Pod deletion test
### Configuration drift test
### Explanation of behaviors

# Screenshots
### ArgoCD UI showing both applications
### Sync status
### Application details view

