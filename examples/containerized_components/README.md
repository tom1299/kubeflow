```
kfp component build . --component-filepattern my_component.py --no-push-image --no-build-image
podman build -t localhost/my-component:v5 .
../../scripts/load-image.sh localhost/my-component:v5
```