# Notes

## Kubeflow installations
### Pods after installation:
```
cache-deployer-deployment-65fb47dd94-829c6        1/1     Running             0             2m58s
cache-server-657b5f8474-vlfks                     0/1     ContainerCreating   0             2m58s
metadata-envoy-deployment-758c78ccb9-6lnfb        1/1     Running             0             2m58s
metadata-grpc-deployment-68d6f447cc-4cp5j         0/1     CrashLoopBackOff    4 (29s ago)   2m58s
metadata-writer-6bf88bb8c4-fw85r                  1/1     Running             0             2m58s
minio-59b68688b5-zqwhj                            1/1     Running             0             2m57s
ml-pipeline-6fd7df65fd-dqrcf                      0/1     Running             1             2m57s
ml-pipeline-persistenceagent-6f86458589-gvzgv     1/1     Running             0             2m57s
ml-pipeline-scheduledworkflow-6d47f64655-kxb2r    1/1     Running             0             2m57s
ml-pipeline-ui-59864db569-l5tl7                   1/1     Running             0             2m57s
ml-pipeline-viewer-crd-c84f488f8-svk9m            1/1     Running             0             2m57s
ml-pipeline-visualizationserver-b688864fb-b6682   1/1     Running             0             2m56s
mysql-5f8cbd6df7-znnbs                            1/1     Running             0             2m56s
workflow-controller-7b46c9c84f-zg4fg              1/1     Running             0             2m56s
```

### Get info abot the cache-server pod
```
kubectl describe pod cache-server-657b5f8474-vlfks
```
Problems in the events:
```
Warning  FailedMount  89s (x9 over 3m36s)  kubelet            MountVolume.SetUp failed for volume "webhook-tls-certs" : secret "webhook-server-tls" not found
```
Mount of the secret:
```
Mounts:
	/etc/webhook/certs from webhook-tls-certs (ro)
```
### Problem with secret disapeared
After some minutes
```
cache-server-657b5f8474-vlfks                     1/1     Running   0             14m
```
Why ?

### Look at the secret
```
kubectl get secrets -n kubeflow
NAME                        TYPE     DATA   AGE
mlpipeline-minio-artifact   Opaque   2      17m
mysql-secret                Opaque   2      17m
webhook-server-tls          Opaque   2      6m48s
```
No annotations, no ownerReferences, no events. So where is the secret coming from ?

### Look at the certificate
See script get-cert-info-from-tls-secret.sh
```
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            03:bd:dd:4f:dc:a1:5f:14:fa:9d:6d:f3:8a:90:b9:90
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: CN = kubernetes
        Validity
            Not Before: Jun  6 06:39:07 2024 GMT
            Not After : Jun  6 06:39:07 2025 GMT
        Subject: O = system:nodes, CN = "system:node:cache-server.kubeflow.svc;"
```
Issuer was Kubernetes itself. So how was the secret created and singed ?

### Explanation
The secret was created by adding a certificatesigningrequests in the cluster:
```
$ kubectl get certificatesigningrequests.certificates.k8s.io -A
NAME                    AGE    SIGNERNAME                                    REQUESTOR                                                             REQUESTEDDURATION   CONDITION
cache-server.kubeflow   96m    kubernetes.io/kubelet-serving                 system:serviceaccount:kubeflow:kubeflow-pipelines-cache-deployer-sa   <none>              Approved,Issued
```
But how was it created and approved. The answer can be found here:
`backend/src/cache/deployer/webhook-create-signed-cert.sh`
In this script the certificate is created and signed by the Kubernetes CA. The certificate is then stored in a secret in the namespace kubeflow. The secret is then used by the cache-server pod.
See also [here](https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/#requesting-a-certificate)


### TODOs
* Learn about `MutatingWebhookConfiguration` which is used to create the certificate and sign it.
* Make a pull request for Kubeflow and convert the secret type from opaque to kubernetes.io/tls.