import logging
import os

import click

from vitaleey_cli.commands.cluster import group as cluster
from vitaleey_cli.commands.docker import group as docker
from vitaleey_cli.commands.gateway import group as api_gateway
from vitaleey_cli.commands.python import group as python
from vitaleey_cli.utils.git import git


@click.group()
def main_group():
    pass


@click.group()
@click.version_option()
@click.option(
    "--debug", is_flag=True, show_default=True, default=False, help="Show debug logging"
)
def main(debug):
    """
    Vitaleey CLI tool

    This tool is used to interact with the Vitaleey API Gateway and Applications.
    If project isn't part of the group Vitaleey, the tool will not work.
    """

    if os.environ.get("CI") and not git.is_repo_part_of("vitaleey"):
        raise click.ClickException(
            "Project is not part of the Vitaleey organization, cannot run commands in CI"
        )

    logger = logging.getLogger("vitaleey_cli")
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter("%(message)s"))

    logger.log(logging.INFO, "Debug logging enabled")
    logger.addHandler(handler)


main.add_command(api_gateway, name="api")
main.add_command(docker, name="docker")
main.add_command(python, name="python")
main.add_command(cluster, name="cluster")
