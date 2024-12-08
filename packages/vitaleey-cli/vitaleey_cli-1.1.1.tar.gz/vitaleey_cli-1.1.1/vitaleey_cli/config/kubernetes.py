from dataclasses import dataclass, field

from .config import CommandConfig, Config, get_env_var

__all__ = ["kubernetes_config"]


@dataclass(frozen=True)
class KubernetesDataclass(CommandConfig):
    """
    Configuration for the application

    Options:
    - cluster_name: The cluster name
    """

    cluster_name: str = get_env_var("KUBERNETES_CLUSTER_NAME", "")
    cluster_id: str = get_env_var("KUBERNETES_CLUSTER_ID", "")
    digitalocean_api_token: str = get_env_var("DIGITALOCEAN_API_TOKEN", "")


@dataclass(frozen=True)
class KubernetesEnvDataclass(CommandConfig):
    """
    Configuration for the application

    Options:
    - cluster_name: The cluster name
    """

    environments: [str, KubernetesDataclass] = field(default_factory=dict)


class KubernetesConfig(Config):
    """
    Kubernetes configuration
    """

    dataclass = KubernetesEnvDataclass
    env_dataclass = KubernetesDataclass


kubernetes_config = KubernetesConfig()
