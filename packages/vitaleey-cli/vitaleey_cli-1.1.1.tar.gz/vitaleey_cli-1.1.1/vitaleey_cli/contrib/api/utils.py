import os

import yaml
from jinja2 import Environment, FileSystemLoader


def read_yaml_file(file):
    """
    Read a YAML file and return the parsed content
    """
    config = None
    with open(file, "r") as f:
        config = f.read()
    return yaml.load(config, Loader=yaml.SafeLoader)


def render_template(template: str, context: dict):
    """
    Render a Jinja2 template with the given context
    """
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")

    env = Environment(loader=FileSystemLoader(templates_dir), autoescape=True)
    template = env.get_template(template)

    return template.render(context)


def filter_dictionary(dictionary: dict):
    """
    Filter out empty values from the dictionary

    Allows boolean values to be set to False
    """

    forbidden = [None, "", [], {}]
    return {k: v for k, v in dictionary.items() if not any([v == f for f in forbidden])}
