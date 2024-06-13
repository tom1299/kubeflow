#!/bin/bash
# This script uses podman to save an image given by its tag and saves it in a tarball.
# The tarball is then loaded into a kind cluster using the kind load
# The only parameter to the script is the image tag.
# The script is a workaround for the issue https://github.com/kubernetes-sigs/kind/issues/2027

# Check if the image tag is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <image-tag>"
  exit 1
fi

# Save the image to a tarball
podman save -o image.tar $1

# Load the image into the kind cluster
kind load image-archive image.tar

# Remove the tarball
rm image.tar
