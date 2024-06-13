import yaml
import sys

def convert_to_debug_pod(pod):
    # Iterate over all containers
    for container in pod['spec']['containers']:
        # Remove liveness, readiness and startup probes
        if 'livenessProbe' in container:
            del container['livenessProbe']
        if 'readinessProbe' in container:
            del container['readinessProbe']
        if 'startupProbe' in container:
            del container['startupProbe']

        # Remove args
        if 'args' in container:
            del container['args']

        # Replace command with a sleep command
        container['command'] = ['sleep', 'infinity']

    # Remove status fields
    if 'status' in pod:
        del pod['status']

    # Remove ownerReferences
    if 'metadata' in pod and 'ownerReferences' in pod['metadata']:
        del pod['metadata']['ownerReferences']

    # Remove pod-template-hash label
    if 'metadata' in pod and 'labels' in pod['metadata'] and 'pod-template-hash' in pod['metadata']['labels']:
        del pod['metadata']['labels']['pod-template-hash']

    # Change the name of the pod
    pod['metadata']['name'] = pod['metadata']['name'] + '-debug'

    return pod

def main():
    if len(sys.argv) != 2:
        print('Usage: convert_to_debug_pod.py <pod-file>')
        sys.exit(1)

    pod_file = sys.argv[1]
    with open(pod_file, 'r') as f:
        pod = yaml.safe_load(f)

    debug_pod = convert_to_debug_pod(pod)

    # Check if the file has .yaml or .yml extension and replace accordingly
    if pod_file.endswith('.yaml'):
        debug_pod_file = pod_file.replace('.yaml', '-debug.yaml')
    elif pod_file.endswith('.yml'):
        debug_pod_file = pod_file.replace('.yml', '-debug.yml')

    with open(debug_pod_file, 'w') as f:
        yaml.dump(debug_pod, f)

    print(yaml.dump(debug_pod))


if __name__ == '__main__':
    main()