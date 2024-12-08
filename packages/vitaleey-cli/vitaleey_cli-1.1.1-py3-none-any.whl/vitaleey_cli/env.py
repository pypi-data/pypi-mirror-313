class EnvironmentNames:
    """
    Environment names and groups for the CLI
    """

    DEVELOPMENT = ["dev", "development"]
    ACCEPTANCE = ["acc", "acceptance"]
    STAGING = ["stg", "staging"]
    QA = ["qa"]
    TEST = ["tst", "test", "testing"]
    PRODUCTION = ["prd", "prod", "production"]

    def groups(self):
        return {
            "development": self.DEVELOPMENT,
            "staging": self.STAGING,
            "qa": self.QA,
            "test": self.TEST,
            "acceptance": self.ACCEPTANCE,
            "production": self.PRODUCTION,
        }

    def get_group(self, name):
        for group, names in self.groups().items():
            if name in names:
                return group

    def get_group_options(self, name):
        """
        Get the group options for a given environment name.
        The option name will be used to select the environment.

        Group: development
            Options: ['dev', 'development']

        Group: acceptance
            Options: ['acc', 'acceptance']

        Group: production
            Options: ['prd', 'prod', 'production']

        Group: staging
            Options: ['stg', 'staging']

        Group: qa
            Options: ['qa']

        Group: test
            Options: ['tst', 'test', 'testing']
        """

        for group, names in self.groups().items():
            if name in names:
                return names

    @staticmethod
    def config_names():
        return ["dev", "acc", "stg", "qa", "tst", "prd"]

    def is_config_name(self, name):
        return name in self.config_names()

    def get_config_name(self, name):
        for c in self.config_names():
            if name == c:
                return c

    def names(self):
        names = []
        for group in self.groups().values():
            names.extend(group)
        return names


environment_names = EnvironmentNames()

ENVIRONMENTS = environment_names.names()
