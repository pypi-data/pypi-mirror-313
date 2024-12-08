from .plugin import Plugin


class ProxyPlugin(Plugin):
    allowed_sections = ["backend", "endpoint"]
    default_options = {
        "sequential": False,
    }
