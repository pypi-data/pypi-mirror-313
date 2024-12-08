import subprocess  # nosec


class Krakend:
    """
    Krakend class to interact with krakend commands
    """

    def __init__(self, config):
        self.config = config

    def check(self):
        cmd = ["krakend", "check", "-c", self.config, "--lint"]
        result = subprocess.run(cmd)  # nosec
        if result.returncode != 0:
            return False
        return True

    def audit(self):
        cmd = ["krakend", "audit", "-c", self.config]
        result = subprocess.run(cmd)  # nosec
        if result.returncode != 0:
            return False
        return True

    def run(self, debug=False):

        if debug:
            cmd = ["krakend", "run", "-dc", self.config]
        else:
            cmd = ["krakend", "run", "-c", self.config]
        result = subprocess.run(cmd)  # nosec
        if result.returncode != 0:
            return False
        return True
