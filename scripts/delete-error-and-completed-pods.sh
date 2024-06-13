#!/bin/bash

# Check if namespace is provided
if [ -z "$1" ]
then
    echo "No namespace supplied. Usage: ./delete_error_completed_pods.sh <namespace>"
    exit 1
fi

NAMESPACE=$1

# Get the names and status of all pods in the namespace
PODS=$(kubectl get pods -n $NAMESPACE -o jsonpath='{range .items[*]}{@.metadata.name} {@.status.phase}{"\n"}{end}')

# Loop over each pod and check its status
while read -r POD STATUS
do
    if [[ $STATUS == "Failed" ]] || [[ $STATUS == "Succeeded" ]]
    then
        echo "Deleting pod $POD with status $STATUS"
        kubectl delete pod $POD -n $NAMESPACE
    else
        echo "Pod $POD is not in Error or Completed state"
    fi
done <<< "$PODS"