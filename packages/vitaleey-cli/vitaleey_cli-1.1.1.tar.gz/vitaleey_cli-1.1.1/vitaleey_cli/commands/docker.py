import json
from uuid import uuid4

import click

from vitaleey_cli.config import application_config
from vitaleey_cli.utils.docker import Docker, DockerException
from vitaleey_cli.utils.git import GitException, git


@click.group(help="Docker helper commands")
def group():
    pass


@group.command()
@click.option("--target", help="Build target")
@click.option("--file", default="Dockerfile", show_default=True)
@click.option("--context", default=".", show_default=True)
@click.option(
    "--push",
    is_flag=True,
    show_default=True,
    default=False,
    help="Push the image to the registry",
)
@click.option("--no-rebuild", is_flag=True, default=False, show_default=True)
def build(**options):
    """
    Build the docker image
    """

    try:
        version = git.latest_commit()
    except GitException as e:
        raise click.UsageError(str(e))

    app_config = application_config()

    docker = Docker(
        registry=app_config.docker_registry,
        image_name=app_config.docker_image_name,
        docker_username=app_config.docker_username,
        docker_password=app_config.docker_password,
    )

    if not do_build(docker, docker.get_image_name(version), options["no_rebuild"]):
        click.secho("Image already exists, skipping build", fg="yellow")
        return

    latest_image = docker.get_image_name(tag=version)

    try:
        docker.pull(latest_image)
    except DockerException:
        latest_image = None

    build_image_tag = uuid4().hex
    try:
        docker.build(
            build_image_tag,
            file=options.get("file"),
            target=options.get("target"),
            cache_from=latest_image,
            context=options.get("context"),
        )
        image = docker.get_image_name(
            tag=version,
        )
        docker.image_tag(build_image_tag, version)
        if options.get("push"):
            docker.push(image)
    except DockerException as e:
        raise click.UsageError(str(e))


@group.command()
@click.argument("src_tag")
@click.argument("new_tag")
def tag(src_tag, new_tag):
    """
    Create a new tag from an existing one
    """

    app_config = application_config()
    docker = Docker(
        registry=app_config.docker_registry,
        image_name=app_config.docker_image_name,
        docker_username=app_config.docker_username,
        docker_password=app_config.docker_password,
    )

    src_image = docker.get_image_name(src_tag)
    new_image = docker.get_image_name(new_tag)

    try:
        manifest = json.loads(docker.manifest("inspect", src_image))
    except DockerException as e:
        raise click.UsageError(f"Could not get src manifest: {e}")

        # Based on manifest get the correct src_image
    if manifest["mediaType"] == "application/vnd.docker.distribution.manifest.v2+json":
        # Valid manifest type for manifest create with standard image path
        pass
    elif (
        manifest["mediaType"]
        == "application/vnd.docker.distribution.manifest.list.v2+json"
    ):
        # Because its a list type we get the first manifest,
        # and use direct digest reference for the create
        src_image = docker.get_image_name() + "@" + manifest["manifests"][0]["digest"]
    else:
        raise click.UsageError(f"Got unkown manifest type: {manifest['mediaType']}")

    # Create new tag
    try:
        docker.manifest("create", new_image, src_image)
    except DockerException as e:
        raise click.UsageError(f"Could not create tag: {e}")

    # Push new tag
    try:
        docker.manifest("push", new_image)
    except DockerException as e:
        raise click.UsageError(f"Could not push image: {e}")

    click.echo(f"New tag created {new_image} from {src_image}")


def do_build(docker: Docker, image: str, no_rebuild: bool):
    if not no_rebuild:
        return True

    try:
        docker.manifest("inspect", image)
        return False
    except DockerException:
        return True
