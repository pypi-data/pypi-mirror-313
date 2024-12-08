import os
import re
from copy import deepcopy

import click
import tomli

from vitaleey_cli.env import environment_names

DEFAULT_CONFIG_FILES = [
    os.path.join(os.getcwd(), "pyproject.toml"),
]


class CommandConfig:
    """
    The base configuration for a command group configuration.
    """

    pass


def get_env_var(name, default=None):
    return os.environ.get("VITALEEY_" + name.upper(), default)


class Config:
    """
    The base configuration for the vitaleey CLI configuration in pyproject.toml.

    NOTE: To retrieve the data call `.load()` on the instance.
    """

    dataclass: CommandConfig | None = None
    env_dataclass: CommandConfig | None = None

    def __init__(
        self,
        main_section: str = "vitaleey",
        skip_dataclass: bool = False,
        skip_command_group: bool = False,
    ):
        self.main_section = main_section
        self.skip_dataclass = skip_dataclass
        self.skip_command_group = skip_command_group

        self._validate_classname()

    def __call__(self, *args, **kwargs):
        environment = kwargs.get("environment")
        section_config = self.load_command_group(self.skip_command_group)

        if environment:
            if environment_names.is_config_name(environment):
                config = self.load_env(section_config, environment)
            else:
                raise click.ClickException(f"Environment {environment} is not valid")
        else:
            config = self.load(section_config, self.skip_dataclass)

        if isinstance(config, dict):
            for k, v in config.items():
                setattr(self, k, v)
        else:
            for k, v in config.__dict__.items():
                setattr(self, k, v)
        return self

    def get_env_dataclass(self):
        return self.env_dataclass

    def get_dataclass(self):
        return self.dataclass

    def _convert_classname(self):
        """
        Get the command group configuration
        """

        return re.sub(r"(?<!^)(?=[A-Z])", "_", self.__class__.__name__).lower()

    def _validate_classname(self):
        if not self._convert_classname().endswith("_config"):
            raise click.ClickException("The class name must end with _config")

    @staticmethod
    def _parse_dataclass(dataclass, config, has_env=False):
        """
        Parse config to dataclass
        """

        if dataclass is not None and config:
            if has_env:
                return dataclass(environments=config)
            return dataclass(**config)
        return config

    @staticmethod
    def remove_env_sections(command_config):
        """
        Remove the environment sections from the configuration
        """

        config = deepcopy(command_config)
        for k, v in command_config.items():
            if environment_names.is_config_name(k):
                del config[k]
        return config

    def load_command_group(self, skip_command_group=False):
        """
        Load the configuration for a command group
        """

        global_config = {}

        for path in DEFAULT_CONFIG_FILES:
            if os.path.exists(path):
                try:
                    with open(path, "rb") as f:
                        global_config = tomli.load(f)
                except tomli.TOMLDecodeError as e:
                    click.ClickException(f"Could not load pyproject.toml file: {e}")
                    global_config = {}

        command_group = self._convert_classname().replace("_config", "")
        config = global_config.get("tool", {}).get(self.main_section, {})
        if not skip_command_group:
            config = config.get(command_group, {})

        return config

    def load_env(self, section_config, environment):
        config = section_config
        envs_config = config.get("envs", {})

        env_dataclass = self.get_env_dataclass()

        # Get environments
        environments = {}

        for group, group_config in envs_config.items():
            options = {
                key: value
                for key, value in group_config.items()
                if key in env_dataclass.__annotations__
            }

            # Set missing options from the main config
            for key in env_dataclass.__annotations__:
                if not options.get(key) and config.get(key):
                    options[key] = config.get(key)

            environments[group] = env_dataclass(**options)

        dataclass = self.get_dataclass()
        if not dataclass:
            raise click.ClickException(
                f"The dataclass is not set for {self.__class__.__name__}"
            )

        parsed_config = self._parse_dataclass(dataclass, environments, has_env=True)
        if not parsed_config:
            raise click.ClickException("Could not load the vitaleey configuration")
        return parsed_config.environments.get(environment)

    def load(self, section_config, skip_dataclass):
        """
        Load the configuration from the pyproject.toml file
        """

        config = section_config
        if skip_dataclass:
            return config

        dataclass = self.get_dataclass()

        for key in dataclass.__annotations__:
            if not config.get(key):
                config[key] = getattr(dataclass, key)

        if not dataclass:
            raise click.ClickException(
                f"The dataclass is not set for {self.__class__.__name__}"
            )

        parsed_config = self._parse_dataclass(dataclass, config)

        if not parsed_config:
            raise click.ClickException("Could not load the vitaleey configuration")
        return parsed_config
