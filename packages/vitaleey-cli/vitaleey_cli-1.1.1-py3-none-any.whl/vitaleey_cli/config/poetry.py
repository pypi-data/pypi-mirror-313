import os

from .config import DEFAULT_CONFIG_FILES, Config

__all__ = ["poetry_config"]


class PoetryConfig(Config):
    """
    Poetry configuration

    Here you can find all the basic project configuration.
    """

    def __init__(self):
        super().__init__("poetry", skip_dataclass=True, skip_command_group=True)

    @staticmethod
    def _change_value(path, section, key, value):
        """
        Update the lines
        """

        lines = []
        at_section = False
        at_end_of_section = False
        for line in open(path, "r"):
            if line.startswith(section):
                at_section = True

            if at_section and not at_end_of_section:
                if line.startswith(key):
                    line = f'{key} = "{value}"\n'

            if at_section and line.startswith("\n"):
                at_end_of_section = True

            lines.append(line)
        return "".join(lines)

    @staticmethod
    def _update_configuration(path, data):
        """
        Update the configuration in the pyproject.toml file
        """

        with open(path, "w") as f:
            f.write(data)

    def set(self, key: str, value: str):
        """
        Set value in the configuration
        """

        for path in DEFAULT_CONFIG_FILES:
            if os.path.exists(path):
                data = self._change_value(path, "[tool.poetry]", key, value)
                self._update_configuration(path, data)
                break  # Only update the first file


poetry_config = PoetryConfig()
