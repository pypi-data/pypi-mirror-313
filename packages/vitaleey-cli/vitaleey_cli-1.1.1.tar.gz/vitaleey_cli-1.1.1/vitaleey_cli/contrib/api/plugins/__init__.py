import copy

import click

from .proxy import ProxyPlugin
from .router import RouterPlugin

plugins = {
    "proxy": ProxyPlugin,
    "router": RouterPlugin,
}


def get_plugin(section, name):

    plugin_class = plugins.get(name)

    if not plugin_class:
        return click.secho(
            f"Skipping plugin {name}, plugin not found at level {section}", fg="yellow"
        )

    return plugin_class


def render_plugin(section: str, data: dict):
    """
    Render the plugin from the data
    """

    _data = copy.deepcopy(data)
    plugin_name = _data.get("name")
    del _data["name"]  # Remove the name from the data
    plugin_class = get_plugin(section, plugin_name)

    if not plugin_class:
        return

    plugin = plugin_class(**_data)
    if plugin.is_valid_section(section):
        return {
            "name": plugin_name,
            "config": plugin.render(),
        }

    return click.secho(
        f"Skipping plugin {plugin_name}, plugin not valid at level {section}",
        fg="yellow",
    )


def render_plugins(section: str, plugin_list: list[dict] = list):
    """
    Render the plugins from the data
    """

    rendered_plugins = {}

    if not plugin_list:
        return rendered_plugins

    for plugin in plugin_list:
        if "name" not in plugin:
            print("Plugin name not found in the plugin data: {}".format(plugin))
            continue

        rendered_plugin = render_plugin(section, plugin)
        if rendered_plugin:
            rendered_plugins[rendered_plugin["name"]] = rendered_plugin["config"]

    return rendered_plugins
