import copy

from .plugins import render_plugins
from .utils import read_yaml_file

PLUGIN_LEVEL = "backend"


class Service:
    """
    A class to represent an API Gateway service
    """

    def __init__(self, service_file):
        self.service_file = service_file

        data = read_yaml_file(service_file)
        self.settings = data.get("settings")
        self.endpoints = data.get("endpoints")

    @property
    def name(self):
        return self.service_file.split("/")[-1].replace(".yaml", "")

    def get_protocol(self):
        """
        Get the protocol for the service
        """

        if self.settings.get("tls_secured"):
            return "https"
        return "http"

    def get_host_port(self, endpoint):
        """
        Get the host and port for the service
        """

        port = self.settings.get("port")
        protocol = self.get_protocol()

        if protocol == "https":
            port = self.settings.get("tls_port", port)

        hostname = self.settings.get("hostname")
        return f"{protocol}://{hostname}:{port}"

    def get_endpoint(self, label):
        """
        Get the endpoint with the given label
        """

        for endpoint in self.endpoints:
            if endpoint.get("label") == label:
                _endpoint = copy.deepcopy(endpoint)
                return _endpoint
        return None

    def get_plugins(self):
        return render_plugins(PLUGIN_LEVEL, self.settings.get("plugins"))

    def render_endpoint(self, label):
        """
        Render the endpoint with the given label
        """

        endpoint = self.get_endpoint(label)
        if not endpoint:
            return None

        plugins = endpoint.get("plugins")
        extra_config = render_plugins(PLUGIN_LEVEL, plugins)
        context = {
            "url_pattern": endpoint.get("url_pattern"),
            "method": endpoint.get("method"),
            "host": [self.get_host_port(endpoint)],
            "extra_config": extra_config,
        }

        return context
