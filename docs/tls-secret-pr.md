# Pull request for changing secret type from opaque to kubernetes.io/tls
1. Build the Docker image of cache server by running the following Docker command from the pipelines directory:
    ```bash
    docker podman build -t cache-deployer-test:1.2.3 -f backend/src/cache/deployer/Dockerfile .
    ```
2. Save the image in a tar file:
    ```bash
    podman save cache-deployer-test:1.2.3 -o cache-deployer-test.tar
    ```
3. Load the image tar into the kind cluster:
    ```bash
    kind load docker-image cache-deployer-test.t
    ```
4. Check whether the image is loaded successfully:
    ```bash
    kind get nodes
    podman exec -it kind-control-plane crictl images
    ```
5. Edit the deployment file:
    ```bash
    kubectl edit deployment cache-deployer-deployment -n kubeflow
    ```
6. Change the image name to the new image name:
    ```yaml
    spec:
      containers:
      - image: cache-deployer-test:1.2.3
        imagePullPolicy: IfNotPresent
    ```
7. Rollout the deployment:
    ```bash
    kubectl rollout restart deployment cache-deployer-deployment -n kubeflow
    ```
