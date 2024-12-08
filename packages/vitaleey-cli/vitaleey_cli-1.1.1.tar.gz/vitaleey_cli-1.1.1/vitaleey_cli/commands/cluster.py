import click

from vitaleey_cli.config import application_config
from vitaleey_cli.config.kubernetes import kubernetes_config
from vitaleey_cli.utils.digitalocean import DigitalOcean
from vitaleey_cli.utils.kubernetes import Kubernetes, KubernetesException


@click.group(help="Kubernetes cluster helper commands")
def group():
    pass


@group.command("registry:add")
@click.option("--docker-registry", help="Docker registry")
@click.option("--docker-username", help="Docker username")
@click.option("--docker-password", help="Docker password")
@click.option("--docker-email", help="Docker email")
@click.option("--cluster_name", help="Kubernetes cluster name")
@click.option("--environment", help="Environment name")
def add_registry(
    environment,
    cluster_name,
    docker_registry,
    docker_username,
    docker_password,
    docker_email,
):
    """
    Add a docker registry for retrieving images for the kubernetes cluster
    """

    app_config = application_config()
    k8_config = kubernetes_config(environment=environment)

    try:
        kubernetes = Kubernetes(
            cluster_name or k8_config.cluster_name,
        )
        registry = kubernetes.set_registry(
            registry_config={
                "docker_registry": docker_registry or app_config.docker_registry,
                "docker_username": docker_username or app_config.docker_username,
                "docker_password": docker_password or app_config.docker_password,
                "docker_email": docker_email or app_config.docker_email,
            }
        )
        if registry:
            click.echo(f"Docker registry {registry} set")
        else:
            raise click.UsageError(
                "Docker registry, username, password and email must be set, run --help for more information"
            )
    except KubernetesException as e:
        raise click.UsageError(str(e))


@group.command("registry:remove")
@click.option("--cluster_name", help="Kubernetes cluster name")
@click.option("--environment", help="Environment name")
@click.argument("registry_name")
def remove_registry(registry_name, environment, cluster_name):
    """
    Remove the docker registry from the kubernetes cluster
    """

    k8_config = kubernetes_config(environment=environment)

    try:
        kubernetes = Kubernetes(
            cluster_name or k8_config.cluster_name,
        )
        registry = kubernetes.remove_registry(registry_name)
        click.echo(registry)
    except KubernetesException as e:
        raise click.UsageError(str(e))


@group.command("registry:list")
@click.option("--cluster_name", help="Kubernetes cluster name")
@click.option("--environment", help="Environment name")
def list_registries(environment, cluster_name):
    """
    List the docker registries in the kubernetes cluster
    """

    k8_config = kubernetes_config(environment=environment)
    do = DigitalOcean(k8_config.digitalocean_api_token)
    kubeconfig_file = do.cluster_config(cluster_name or k8_config.cluster_name)

    try:
        kubernetes = Kubernetes(
            kubeconfig_file=kubeconfig_file,
        )
        registries = kubernetes.list_registries()
        click.echo(registries)
    except KubernetesException as e:
        raise click.UsageError(str(e))


@group.command("nodes")
@click.argument("environment")
def get_nodes(environment):
    """
    Get the kubernetes nodes
    """

    k8_config = kubernetes_config(environment=environment)
    cluster_name = k8_config.cluster_name

    if not cluster_name:
        raise click.UsageError("Cluster name must be set in the configuration")

    try:
        kubernetes = Kubernetes(
            cluster_name,
        )
        nodes = kubernetes.get_nodes()
        click.echo(nodes)
    except KubernetesException as e:
        raise click.UsageError(str(e))
