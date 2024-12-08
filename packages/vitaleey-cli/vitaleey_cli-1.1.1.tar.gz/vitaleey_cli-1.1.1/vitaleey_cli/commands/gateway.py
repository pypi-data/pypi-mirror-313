import click

from vitaleey_cli.contrib.api.gateway import Gateway

DEFAULT_CONFIG_PATH = "./config"


@click.group(help="API Gateway helper commands")
def group() -> click.Command:
    pass


@group.command(name="services", help="List all API Gateway resources")
@click.option("--config_path", help="Config file path", default=DEFAULT_CONFIG_PATH)
def show_services(config_path):

    gateway = Gateway(config_path)
    services = gateway.get_services()

    click.secho("Listing API Gateway services\n", bold=True)

    for service in services:
        click.echo(f"Service: {service['name']}")
        for key, value in service["data"]["settings"].items():
            click.echo(f"{key.title()}: {value}")
        click.echo(f"Endpoints: {len(service['data']['endpoints'])}\n")


@group.command(name="settings", help="Show API Gateway settings")
@click.option("--config_path", help="Config file path", default=DEFAULT_CONFIG_PATH)
def show_settings(config_path):

    gateway = Gateway(config_path)
    settings = gateway.get_settings()

    click.secho("Show API Gateway settings\n", bold=True)

    for key, value in settings.items():
        click.echo(f"{click.style(f"{key}: ", fg="blue")}{value}")


@group.command(name="endpoints", help="Show API Gateway endpoints")
@click.option("--service", "-s", help="Filter by service")
@click.option("--config_path", help="Config file path", default=DEFAULT_CONFIG_PATH)
def show_endpoints(service, config_path):
    gateway = Gateway(config_path)
    endpoints = gateway.get_endpoints()

    click.secho("Show API Gateway endpoints\n", bold=True)

    if service:
        endpoints = gateway.get_service_endpoints(service)

    for endpoint in endpoints:
        click.echo(f"* Endpoint: {endpoint.endpoint}")
        click.echo(f"  Method: {endpoint.method}")
        click.echo(f"  Extra Config: {endpoint.extra_config}")
        click.echo("  Backends:")
        for backend in endpoint.backends:
            click.echo(f"  * Service: {backend.service}")
            click.echo(f"  * URL Pattern: {backend.url_pattern}")
            click.echo(f"  * Extra Config: {backend.extra_config}\n")


@group.command()
@click.option("--config_path", help="Config file path", default=DEFAULT_CONFIG_PATH)
def audit(config_path):
    """
    Audit the Kraken API Gateway file
    """

    click.secho("Audit the Kraken API Gateway file \n", bold=True)

    gateway = Gateway(config_path)
    gateway.audit()


@group.command()
@click.option("--config_path", help="Config file path", default=DEFAULT_CONFIG_PATH)
@click.option(
    "--set_as_file", is_flag=True, help="Force the file to be written as a file"
)
@click.argument("output", default=".")
def export(output, set_as_file, config_path):
    """
    Export the Kraken API Gateway file
    """

    click.secho("Export the Kraken API Gateway file \n", bold=True)

    gateway = Gateway(config_path)

    filename = gateway.export(output, set_as_file)

    click.secho(f"Exported to {filename}", fg="green")


@group.command()
@click.option("--debug", is_flag=True, help="Enable debugging endpoints")
@click.option("--config_path", help="Config file path", default=DEFAULT_CONFIG_PATH)
def run(config_path, debug):
    """
    Run the Kraken API Gateway file
    """

    click.secho("Run the Kraken API Gateway file \n", bold=True)

    click.secho(
        "By default plugins set at service level will be set at service_endpoint level if they have none\n",
        bold=True,
    )
    click.secho(
        "!IMPORTANT!: \
        \n  - Plugins set at backend level will override the plugins set at service_endpoint level \
        \n  - Plugins set at service_endpoint level will override the plugins set at service level",
        fg="yellow",
    )

    gateway = Gateway(config_path)
    gateway.run(debug=debug)
