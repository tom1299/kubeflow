#!/bin/bash

# Check if namespace is provided
if [ -z "$1" ]
then
    echo "No namespace supplied. Usage: ./delete_terminating_pods.sh <namespace>"
    exit 1
fi

NAMESPACE=$1

# Get the names of all pods in the namespace
PODS=$(kubectl get pods -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}')

# Loop over each pod and check its status
for POD in $PODS
do
    DESCRIPTION=$(kubectl describe pod $POD -n $NAMESPACE)
    if [[ $DESCRIPTION =~ Status:.*Terminating.* ]]
    then
        echo "Force deleting pod $POD"
        kubectl delete pod $POD -n $NAMESPACE --grace-period=0 --force
    else
        echo "Pod $POD is not in Terminating state"
    fi
done