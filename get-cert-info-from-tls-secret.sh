#!/bin/bash
# This script writes the content of a certificate stored
# in a k8s tls secret.
# The script first uses kubectl to get the secret and extract the pem.
# Then it uses openssl to extract the certificate information.
# Usage: get-cert-info-from-tls-secret.sh <namespace> <secret-name>

if [ "$#" -ne 2 ]; then
    echo "Usage: get-cert-info-from-tls-secret.sh <namespace> <secret-name>"
    exit 1
fi

namespace=$1
secret_name=$2

# Get the secret and directly pass it to openssl
kubectl get secret "$secret_name" -n "$namespace" -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout
