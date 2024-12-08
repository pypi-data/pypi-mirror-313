import logging
import os
import subprocess
import tempfile

logger = logging.getLogger(__name__)


class KubernetesException(Exception):
    pass


class Kubernetes:
    """
    Kubernetes class to interact with kubectl commands
    """

    def __init__(self, kubeconfig_file):
        self._registry_set = False
        self._kubeconfig_file = kubeconfig_file

    @property
    def registry_set(self):
        return self._registry_set

    def run(self, command: list, kubectl=True):
        cli_command = "kubectl"
        if kubectl:
            if command[0] != cli_command:
                command = [cli_command] + command
            command.append(f"--kubeconfig={self._kubeconfig_file}")

            logger.debug(f"Running kubectl command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise KubernetesException(f"Executing {command}:\n\n{result.stderr}")

        logger.debug(result.stdout)
        return result.stdout

    def get_digitalocean_cluster_kubeconfig(self, digitalocean_cluster_name):
        logger.debug("Get digitalocean cluster kubeconfig")

        file = os.path.join(tempfile.gettempdir(), "kubeconfig")
        result = self.run(
            [
                "doctl",
                "kubernetes",
                "cluster",
                "kubeconfig",
                "show",
                digitalocean_cluster_name,
            ],
            kubectl=False,
        )

        with open(file, "w") as f:
            f.write(result)
        return file

    def get_nodes(self):
        logger.info("Get kubernetes nodes")
        return self.run(["get", "nodes"])

    def exists_registry(self, registry_name):
        logger.info("Check if docker registry exists in kubernetes")

        try:
            self.run(["get", "secret", registry_name, "-o", "json"])
        except KubernetesException:
            return False
        return True

    def list_registries(self):
        logger.info("List docker registries in kubernetes")

        return self.run(
            ["get", "secrets", "--field-selector=type=kubernetes.io/dockerconfigjson"]
        )

    def remove_registry(self, registry_name):
        logger.info("Remove docker registry from kubernetes")

        if not self.exists_registry(registry_name):
            raise KubernetesException(f"Docker registry {registry_name} does not exist")

        return self.run(["delete", "secret", registry_name])

    def set_registry(self, registry_config):
        logger.info("Set docker registry for kubernetes")

        if any(not cred for cred in registry_config.values()):
            return

        docker_registry = registry_config.get("docker_registry")
        docker_username = registry_config.get("docker_username")
        docker_password = registry_config.get("docker_password")
        docker_email = registry_config.get("docker_email")

        registry_name = docker_registry.replace("/", "-")
        if self.exists_registry(registry_name):
            raise KubernetesException(f"Docker registry {registry_name} already exists")

        return self.run(
            [
                "create",
                "secret",
                "docker-registry",
                registry_name,
                f"--docker-server={docker_registry}",
                f"--docker-username={docker_username}",
                f"--docker-password={docker_password}",
                f"--docker-email={docker_email}",
            ]
        )
