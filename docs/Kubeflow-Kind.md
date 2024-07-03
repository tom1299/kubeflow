# Kubeflow with kind and podman
* After cluster creation use `podman start kind-control-plane kind-worker kind-worker2` to restart the cluster
* **TODO:** This starts a single container cluster. How does this work with cluster with multiple nodes / containers

commands:
```
podman start kind-control-plane kind-worker kind-worker2
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
```
