import logging
import subprocess

logger = logging.getLogger(__name__)


class DockerException(Exception):
    pass


class Docker:
    """
    Docker class to interact with docker commands
    """

    def __init__(self, registry, image_name, docker_username, docker_password):
        self._registry = registry
        self._image_name = image_name
        self._docker_username = docker_username
        self._docker_password = docker_password
        self._logged_in = False

    def run(self, command: list):
        self.login()

        if command[0] != "docker":
            command = ["docker"] + command

        logger.debug(f"Running docker command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise DockerException(f"Executing {command}:\n\n{result.stderr}")

        logger.debug(result.stdout)
        return result.stdout

    def login(self):
        if self._logged_in or not self._docker_username or not self._docker_password:
            return

        logger.debug(
            f"Docker login to {self._registry} with user {self._docker_username}"
        )
        result = subprocess.run(
            [
                "docker",
                "login",
                self._registry,
                f"--username={self._docker_username}",
                f"--password={self._docker_password}",
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise ConnectionError(
                f"Could not login to {self._registry} with user {self._docker_username}: {result.stderr}"  # noqa: E501
            )
        self._logged_in = True

    def build(self, tag, file="Dockerfile", target=None, cache_from=None, context="."):
        logger.info(f"Docker build image {tag}")
        logger.info(f" - context={context}")
        logger.info(f" - target={target}")
        logger.info(f" - cache_from={cache_from}")
        return self.run(
            list(
                filter(
                    None,
                    [
                        "build",
                        "--pull",
                        f"--target={target}" if target else None,
                        f"--file={file}",
                        f"--tag={self._image_name}:{tag}",
                        f"--cache-from={cache_from}" if cache_from else None,
                        context,
                    ],
                )
            )
        )

    def push(self, image):
        logger.info(f"Pushing {image}")
        return self.run(["image", "push", f"{image}"])

    def pull(self, tag):
        return self.run(["pull", tag])

    def image_tag(self, tag, new_tag):
        logger.info(f"Docker create tag {tag} -> {new_tag}")
        return self.run(
            [
                "image",
                "tag",
                f"{self._image_name}:{tag}",
                f"{self._image_name}:{new_tag}",
            ]
        )

    def manifest(self, *args):
        return self.run(["manifest", *args])

    def get_image_name(self, tag=None):
        return f"{self._image_name}:{tag}" if tag else self._image_name
