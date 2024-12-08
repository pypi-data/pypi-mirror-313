from dataclasses import dataclass

from .config import CommandConfig, Config, get_env_var

__all__ = ["application_config"]

DEFAULT_PYTHON_REGISTRY = "registry.gitlab.com/vitaleey"
DEFAULT_DOCKER_REGISTRY = "registry.gitlab.com/vitaleey"
DEFAULT_DOCKER_EMAIL = "admin@vitaleey.com"


@dataclass(frozen=False)
class ApplicationDataclass(CommandConfig):
    """
    Configuration for the application

    Options:
    - python_registry: The python registry
    - python_username: The python username
    - python_password: The python password
    - pypi_token: The pypi token

    - docker_registry: The docker registry
    - docker_email: The docker email
    - docker_password: The docker password
    - docker_username: The docker username
    - docker_image_name: The docker image name
    """

    python_registry: str = get_env_var("PYTHON_REGISTRY", DEFAULT_PYTHON_REGISTRY)
    python_username: str = get_env_var("PYTHON_USERNAME", "")
    python_password: str = get_env_var("PYTHON_PASSWORD", "")
    pypi_token: str = get_env_var("PYPI_TOKEN", "")

    docker_registry: str = get_env_var("DOCKER_REGISTRY", DEFAULT_DOCKER_REGISTRY)
    docker_email: str = get_env_var("DOCKER_EMAIL", DEFAULT_DOCKER_EMAIL)
    docker_password: str = get_env_var("DOCKER_PASSWORD", "")
    docker_username: str = get_env_var("DOCKER_USERNAME", "")
    docker_image_name: str = get_env_var("DOCKER_IMAGE_NAME", "")


class ApplicationConfig(Config):
    """
    Application configuration
    """

    dataclass = ApplicationDataclass


application_config = ApplicationConfig()
