import click

from vitaleey_cli.config import application_config, poetry_config
from vitaleey_cli.utils.git import GitException, git
from vitaleey_cli.utils.poetry import poetry


@click.group(help="Python helper commands")
def group():
    pass


def release_package(latest_tag, registry):
    """
    Release package and publish it to GitLab registry
    """

    version = latest_tag.lstrip("v")
    poetry_config.set("version", version)

    click.secho(f"Updated the version to {version}", fg="green", bold=True)

    if not poetry.publish_package(registry == "pypi"):
        raise click.ClickException("Failed to publish package")

    try:
        git.new_version(latest_tag)
    except GitException as e:
        raise click.UsageError(str(e))
    click.secho("Package published", fg="green")


@group.command()
def release():
    """
    Release application and publish it to GitLab registry
    """

    app_config = application_config()

    try:
        latest_tag = git.latest_tag()
    except GitException as e:
        raise click.UsageError(str(e))

    pc = poetry_config()
    if latest_tag.lstrip("v") == pc.version:
        click.secho(f"No new release found, still version {latest_tag}", fg="yellow")
        return

    click.secho(f"New release found: {latest_tag}", fg="green")

    release_package(latest_tag, app_config.python_registry)
