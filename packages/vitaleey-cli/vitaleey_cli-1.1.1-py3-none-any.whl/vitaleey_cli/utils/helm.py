import logging
import subprocess

logger = logging.getLogger(__name__)


class HelmException(Exception):
    pass


class Helm:
    """
    Helm class to interact with helm commands
    """

    def __init__(self, kube_config_file):
        self._kubeconfig_file = kube_config_file

    def run(self, command: list):
        cli_command = "helm"
        if command[0] != cli_command:
            command = [cli_command] + command
        command.append(f"--kubeconfig={self._kubeconfig_file}")

        logger.debug(f"Running {cli_command} command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise HelmException(f"Executing {command}:\n\n{result.stderr}")

        logger.debug(result.stdout)
        return result.stdout

    def list_repos(self, namespace=None):
        logger.info("List helm repos in the cluster")

        namespace_arg = f"--namespace={namespace}" if namespace else None
        return self.run(["repo", "list", namespace_arg])

    def add_repo(self, repo_name, repo_url, namespace=None):
        logger.info(f"Add helm repo {repo_name} to the cluster")

        namespace_arg = f"--namespace={namespace}" if namespace else None
        return self.run(["repo", "add", repo_name, repo_url, namespace_arg])

    def install_chart(
        self, chart_name, chart_version, release_name, namespace=None, values_file=None
    ):
        logger.info(f"Install helm chart {chart_name} in the cluster")

        namespace_arg = f"--namespace={namespace}" if namespace else None
        values_arg = f"--values={values_file}" if values_file else None
        return self.run(
            [
                "install",
                release_name,
                chart_name,
                "--version",
                chart_version,
                namespace_arg,
                values_arg,
            ]
        )

    def upgrade_chart(
        self, chart_name, chart_version, release_name, namespace=None, values_file=None
    ):
        logger.info(f"Upgrade helm chart {chart_name} in the cluster")

        namespace_arg = f"--namespace={namespace}" if namespace else None
        values_arg = f"--values={values_file}" if values_file else None
        return self.run(
            [
                "upgrade",
                release_name,
                chart_name,
                "--version",
                chart_version,
                namespace_arg,
                values_arg,
            ]
        )
