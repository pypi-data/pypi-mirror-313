import logging
import subprocess
import os
import tempfile

logger = logging.getLogger(__name__)


class DigitalOceanException(Exception):
    pass


class DigitalOcean:
    def __init__(self, access_token):
        self.access_token = access_token

    @staticmethod
    def run(command: list):
        cli_command = "doctl"

        if command[0] != cli_command:
            command = [cli_command] + command

        logger.debug(f"Running {cli_command} command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise DigitalOceanException(f"Executing {command}:\n\n{result.stderr}")

        logger.debug(result.stdout)
        return result.stdout

    def cluster_config(self, cluster_name):
        logger.debug("Get digitalocean cluster kubeconfig")

        file = os.path.join(tempfile.gettempdir(), "kubeconfig")
        result = self.run(
            [
                "kubernetes",
                "cluster",
                "kubeconfig",
                "show",
                cluster_name,
                f"--access-token={self.access_token}",
            ],
        )

        with open(file, "w") as f:
            f.write(result)
        return file
