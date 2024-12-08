import subprocess

import click

from vitaleey_cli.config import application_config


class Poetry:
    """
    Poetry class to handle poetry commands
    """

    def __init__(self):
        self._repository = "gitlab"

    def publish_package(self, to_pypi=False):
        if to_pypi:
            if not self._publish_to_pypi():
                raise click.ClickException("Failed to publish to pypi")
        else:
            if not self.set_repository():
                raise click.ClickException("Failed to set repository auth")

            if not self.set_repository_auth():
                raise click.ClickException("Failed to set repository auth")

            if not self._publish_to_repository():
                raise click.ClickException("Failed to publish to repository")
        return True

    def _publish_to_repository(self):
        cmd = ["poetry", "publish", "--build", "--repository", self._repository]
        result = subprocess.run(cmd)
        if result.returncode != 0:
            return False
        return True

    def _enable_pypi_auth(self):
        app_config = application_config()
        pypi_token = app_config.pypi_token

        if pypi_token is None:
            raise click.ClickException("VITALEEY_PYPI_TOKEN is not set")

        cmd = ["poetry", "config", "pypi-token.pypi", pypi_token]
        result = subprocess.run(cmd)
        if result.returncode != 0:
            return False
        return True

    def _publish_to_pypi(self):
        if not self._enable_pypi_auth():
            raise click.ClickException("Failed to enable pypi auth")

        cmd = ["poetry", "publish", "--build"]
        result = subprocess.run(cmd)
        if result.returncode != 0:
            return False
        return True

    def set_repository_auth(self):
        app_config = application_config()

        cmd = [
            "poetry",
            "config",
            f"http-basic.{self._repository}",
            app_config.python_username,
            app_config.python_password,
        ]
        result = subprocess.run(cmd)
        if result.returncode != 0:
            return False
        return True

    def set_repository(self):
        app_config = application_config()

        cmd = [
            "poetry",
            "source",
            "add",
            "--priority=supplemental",
            "gitlab",
            app_config.python_registry,
        ]
        result = subprocess.run(cmd)
        if result.returncode != 0:
            return False
        return True


poetry = Poetry()
