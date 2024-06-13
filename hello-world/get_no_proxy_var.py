import argparse
from kubernetes import client


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apiserver', required=True, help='API server URL')
    parser.add_argument('--namespaces', required=True, help='Comma-separated list of namespaces')
    args = parser.parse_args()

    return get_no_proxy_var(args.apiserver, args.namespaces.split(','))


def get_no_proxy_var(apiserver, namespaces):

    configuration = client.Configuration()
    configuration.host = apiserver
    configuration.verify_ssl = False
    client.Configuration.set_default(configuration)
    v1 = client.CoreV1Api()

    no_proxy_var = ""

    for namespace in namespaces:
        services = v1.list_namespaced_service(namespace)

        for service in services.items:
            # Get the IP, short DNS name, and long DNS name
            ip = service.spec.cluster_ip
            short_dns_name = service.metadata.name
            long_dns_name = f"{short_dns_name}.{namespace}.svc.cluster.local"

            # Append the values to the no_proxy_var string
            no_proxy_var += f"{ip},{short_dns_name},{long_dns_name},"

    print(no_proxy_var)
    return no_proxy_var


if __name__ == '__main__':
    main()