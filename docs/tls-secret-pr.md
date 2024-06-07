# Pull request for changing secret type from opaque to kubernetes.io/tls
1. Build the Docker image of cache server by running the following Docker command from the pipelines directory:
    ```bash
    docker build -t gcr.io/ml-pipeline/cache-server-test:1.2.3 -f backend/Dockerfile.cacheserver .
    ```
2. Save the image in a tar file:
    ```bash
    podman save gcr.io/ml-pipeline/cache-server-test:1.2.3 -o cache-server-test.tar
    ```
3. Load the image tar into the kind cluster:
    ```bash
    kind load docker-image cache-server-test.tar
    ```
4. Check whether the image is loaded successfully:
    ```bash
    kind get nodes
    docker exec -it kind-control-plane crictl images
    ```
5. Edit the deployment file:
    ```bash
    kubectl edit deployment cache-server -n kubeflow
    ```
6. Change the image name to the new image name:
    ```yaml
    spec:
      containers:
      - image: gcr.io/ml-pipeline/cache-server-test:1.2.3
    ```
7. Rollout the deployment:
    ```bash
    kubectl rollout restart deployment cache-server -n kubeflow
    ```
