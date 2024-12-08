import copy

ALLOWED_SECTIONS_CHOICES = [
    "endpoint",
    "settings",
    "backend",
]


class Plugin:
    default_options = {}
    allowed_sections = ALLOWED_SECTIONS_CHOICES

    def __init__(self, **options):
        self.options = options

        self.__validate_allowed_sections()

    def get_default_options(self):
        """
        Get the default options for the plugin
        """

        return self.default_options

    def __validate_allowed_sections(self):
        """
        Validate the allowed sections
        """

        allowed_sections = self.get_allowed_sections()
        if not self.allowed_sections:
            raise ValueError("Allowed sections not defined")

        if not all(section in ALLOWED_SECTIONS_CHOICES for section in allowed_sections):
            raise ValueError(
                f"Invalid allowed sections ({allowed_sections}), choices: {ALLOWED_SECTIONS_CHOICES}"
            )

    def get_allowed_sections(self):
        """
        Get the allowed sections for the plugin
        """

        return self.allowed_sections

    def is_valid_section(self, section):
        """
        Check if the section is valid
        """

        return section in self.get_allowed_sections()

    def render(self):
        """
        Render the plugin
        """

        _options = copy.deepcopy(self.options)
        for key, value in _options.items():
            if key in self.get_default_options():
                _options[key] = value
        return _options
