import json
import os
import tempfile
from dataclasses import dataclass, field

import click

from vitaleey_cli.utils.krakend import Krakend

from .plugins import render_plugins
from .service import Service
from .settings import settings as default_settings
from .utils import filter_dictionary, read_yaml_file, render_template


@dataclass(frozen=False)
class GatewayEndpoint:
    """
    Configuration for an APIGateway endpoint
    """

    endpoint: str = ""
    method: str = "GET"
    description: str = ""
    extra_config: list[dict] = field(default_factory=list)
    backends: list[dict] = field(default_factory=list)
    input_headers: list[str] = field(default_factory=list)
    input_query_strings: list[str] = field(default_factory=list)
    cache_ttl: str = ""


class Gateway:
    """Gateway class for generating API requests"""

    def __init__(self, config_dir):
        self._temporary_dir = tempfile.mkdtemp()
        self._config_dir = os.path.join(os.getcwd(), config_dir)

        # Set the output directory
        self._file_output_dir = self._temporary_dir

        self._filename = os.path.abspath(
            os.path.join(self._file_output_dir, "gateway.json")
        )

        self._gateway_file = os.path.abspath(
            os.path.join(self._config_dir, "gateway.yaml")
        )

        if not os.path.exists(self._gateway_file):
            raise click.ClickException(
                click.style(
                    f"Gateway file not found, please create the {self._gateway_file} file",
                    fg="red",
                )
            )
        self._data = read_yaml_file(self._gateway_file)

    def write_config_file(self, data):
        """
        Write the data to the config file
        """

        dirname = os.path.dirname(self._filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(self._filename, "w") as f:
            f.write(data)

        return self._filename

    def get_settings(self):
        """
        Return the settings for the gateway
        """

        section = "settings"
        settings = self._data.get("settings")

        for key, value in default_settings.items():
            if key not in settings:
                settings[key] = value

        settings["extra_config"] = json.dumps(
            render_plugins(section, settings.get("plugins")), indent=2
        )
        return filter_dictionary(settings)

    def get_endpoints(self):
        """
        Return a list of GatewayEndpoint objects
        """

        endpoints = []

        data_endpoints = self._data.get("endpoints") or []
        for endpoint in data_endpoints:
            backends = []
            for backend in endpoint.get("backends"):
                backends.append(backend)

            section = "endpoint"
            extra_config = render_plugins(section, endpoint.get("plugins"))
            gateway_endpoint = GatewayEndpoint(
                endpoint=endpoint.get("endpoint"),
                method=endpoint.get("method"),
                description=endpoint.get("description"),
                extra_config=extra_config,
                input_headers=endpoint.get("input_headers"),
                input_query_strings=endpoint.get("input_query_strings"),
                backends=backends,
            )

            endpoints.append(gateway_endpoint)
        return endpoints

    def get_service_endpoints(self, service_name):
        """
        Return a list of GatewayEndpoint objects for a given service name
        """

        endpoints = []
        for endpoint in self.get_endpoints():
            for backend in endpoint.backends:
                if backend["service"] == service_name:
                    endpoints.append(endpoint)
        return endpoints

    def get_services(self):
        """
        Return a list of Service objects
        """

        services = []
        service_dir = os.path.join(self._config_dir, "services")

        for service_file in os.listdir(service_dir):
            if not service_file.endswith(".yaml"):
                continue
            service = Service(os.path.join(service_dir, service_file))
            services.append(service)
        return services

    def _get_service(self, service_name):
        """
        Return the service object for a given service name
        """

        for service in self.get_services():
            if service.name == service_name:
                return service
        return None

    def render_backend(self, backend):
        """
        Render the backend for the gateway
        """

        service = self._get_service(backend["service"])
        rendered_endpoint = service.render_endpoint(backend["url_pattern"])
        context = filter_dictionary(
            {
                **rendered_endpoint,
                "allow": backend.get("allow", []),
                "deny": backend.get("deny", []),
                "disable_host_sanitize": backend.get("disable_host_sanitize", False),
                "encoding": backend.get("encoding", "no-op"),
                "group": backend.get("group", ""),
                "input_headers": backend.get("input_headers", []),
                "is_collection": backend.get("is_collection", True),
                "mapping": backend.get("mapping", {}),
                "sd": backend.get("sd", "static"),
                "sd_scheme": service.get_protocol(),
                "target": backend.get("target", ""),
            }
        )

        if "extra_config" not in context:
            context["extra_config"] = service.get_plugins()
        return filter_dictionary(context)

    def render_endpoints(self):
        """
        Render the endpoints for the gateway
        """

        endpoints = self.get_endpoints()
        rendered_endpoints = []

        section = "backend"
        for endpoint in endpoints:
            backends = []
            for backend in endpoint.backends:
                rendered_backend = self.render_backend(backend)

                if "plugins" in backend:
                    # Override the extra config with the backend plugins
                    rendered_backend["extra_config"] = render_plugins(
                        section, rendered_backend.get("plugins")
                    )
                backends.append(rendered_backend)
            context = filter_dictionary(
                {
                    "endpoint": endpoint.endpoint,
                    "method": endpoint.method,
                    "@comment": endpoint.description,
                    "extra_config": endpoint.extra_config,
                    "input_headers": endpoint.input_headers,
                    "input_query_strings": endpoint.input_query_strings,
                    "backend": backends,
                }
            )

            rendered_endpoints.append(context)
        return rendered_endpoints

    def cleanup(self):
        """
        Remove the temporary gateway file
        """

        for root, _, files in os.walk(self._temporary_dir):
            for file in files:
                os.remove(os.path.join(root, file))
        os.removedirs(self._temporary_dir)

    def render_config(self):
        """
        Render the gateway configuration
        """

        settings = self.get_settings()
        endpoints = self.render_endpoints()

        context = {
            "settings": settings,
            "endpoints": endpoints,
        }

        return render_template("gateway.j2", context)

    def create_gateway_file(self):
        """
        Create the gateway file in the output directory
        """

        content = self.render_config()

        # Write the content to the gateway file
        return self.write_config_file(content)

    def _check(self):
        """
        Check if the gateway file is valid
        """

        filename = self.create_gateway_file()

        krakend = Krakend(filename)
        result = krakend.check()

        return result

    def audit(self):
        """
        Audit the gateway file
        """

        filename = self.create_gateway_file()

        krakend = Krakend(filename)
        result = krakend.audit()
        self.cleanup()  # Remove the temporary file

        if not result:
            raise click.ClickException(
                click.style(
                    "KrakenD audit failed, please solve the vulnerabilities", fg="red"
                )
            )
        self.cleanup()  # Remove the temporary file

    def export(self, output, set_as_file=False):
        """
        Export the gateway file
        """

        if not self._check():
            raise click.ClickException(
                click.style(
                    "KrakenD check failed, please solve the configuration errors",
                    fg="red",
                )
            )

        output = os.path.abspath(os.path.join(os.getcwd(), output))

        set_as_file = set_as_file or os.path.splitext(output)[1] == ".json"

        if not set_as_file:
            if not os.path.exists(output):
                os.makedirs(output)

            output = os.path.join(output, "gateway.json")

        if output:
            if os.path.exists(output) and os.path.isdir(output):
                raise click.ClickException(
                    click.style(
                        f"Directory {output} exists, please remove it",
                        fg="red",
                    )
                )

            with open(self._filename, "r") as f:
                data = f.read()

            with open(output, "w") as f:
                f.write(data)

        return output

    def run(self, debug=False):
        """
        Run the gateway file
        """

        if not self._check():
            raise click.ClickException(
                click.style(
                    "KrakenD check failed, please solve the configuration errors",
                    fg="red",
                )
            )

        krakend = Krakend(self._filename)

        try:
            result = krakend.run(debug)
            if not result:
                raise click.ClickException(
                    click.style(
                        "KrakenD run failed, please solve the runtime errors", fg="red"
                    )
                )
        except KeyboardInterrupt:
            print("KrakenD stopped")
            self.cleanup()  # Remove the temporary file
