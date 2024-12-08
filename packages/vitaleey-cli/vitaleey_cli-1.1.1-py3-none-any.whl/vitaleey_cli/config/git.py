from dataclasses import dataclass

from .config import CommandConfig, Config, get_env_var

__all__ = ["gitlab_config"]

DEFAULT_BRANCH = "main"


@dataclass(frozen=False)
class GitlabDataclass(CommandConfig):
    """
    Configuration for Git

    Options:
    - branch: The target branch
    - project_id: The project ID
    - private_token: The private token
    """

    branch: str = get_env_var("GITLAB_BRANCH", DEFAULT_BRANCH)
    project_id: str = get_env_var("GITLAB_PROJECT_ID", "")
    private_token: str = get_env_var("GITLAB_PRIVATE_TOKEN", "")


class GitlabConfig(Config):
    """
    Git configuration
    """

    dataclass = GitlabDataclass


gitlab_config = GitlabConfig()
