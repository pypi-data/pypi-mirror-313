"""
Defines a Skyramp client, which can be used to interact with a cluster.
"""

from typing import Optional
from skyramp.docker_client import _DockerClient
from skyramp.k8s_client import _K8SClient

def _client(kubeconfig_path: Optional[str]="",
            kubeconfig_context: Optional[str]="",
            cluster_name: Optional[str]="",
            namespace: Optional[str]="",
            worker_address: Optional[str]="",
            docker_network: Optional[str]=""):
    """
    Create Skyramp Client
    if worker_address is provided, it creates a docker client
    if one of kubeconfig_path, k8s_context, cluster_name, and/or namespace is given, 
    it creates a k8s client
    """
    if worker_address != "" and (namespace != "" or
             kubeconfig_path != "" or kubeconfig_context != "" or cluster_name != ""):
        raise Exception("Address cannot be used with k8s related parameters")
    if worker_address == "" and namespace == "" and \
            kubeconfig_path  == "" and kubeconfig_context == "" and cluster_name == "":
        raise Exception("Either address or k8s related parameters should be given")

    if worker_address != "":
        return _DockerClient(worker_address, network_name=docker_network)

    return _K8SClient(kubeconfig_path, cluster_name, kubeconfig_context, namespace)
