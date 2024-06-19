# add_v1.py
## Get the script to work
* Works with version 1.8.5 of kfp
* Steps to install kfp v1.8.5 (requires fixing dependencies):
  * Install python 3.11
  * Create venv: `python3.11 -m venv ".venv"`
  * Install pyyaml: `pip install "cython<3.0.0" wheel && pip install pyyaml==5.4.1 --no-build-isolation`
  * Install kfp: `pip install kfp==1.8.5`
  * Install requests fix: `pip install urllib3==1.26.15 requests-toolbelt==0.10.1`
## Create the cluster
```
export PIPELINE_VERSION=1.8.5
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"
```
Forward the ui port:
```
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
```

# hello_world_v1.py
## Get the script to work
* TODO: Add instructions to get the script to work
## Create the cluster
* TODO: Add instructions to create the cluster
