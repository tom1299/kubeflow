import argparse

from kubernetes import client

import os


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


http_proxy=os.getenv('http_proxy')
https_proxy=os.getenv('https_proxy')
no_proxy=os.getenv('no_proxy') + "," + get_no_proxy_var("https://127.0.0.1:6443", ["default", "kubeflow"])


def add_proxy_env_vars(function):
    function.set_env_variable('http_proxy', http_proxy).set_env_variable('https_proxy', https_proxy).set_env_variable('no_proxy', no_proxy)
