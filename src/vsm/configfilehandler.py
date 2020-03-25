from os import path
from pickle import load
from pickle import dump

from .config import Config

class ConfigFileHandler:
    """
    file handler for config objects
    """

    def __init__(self, configFile, directory=""):
        """
        configFile -> file name.
        directory -> directory to store config file.
        """
        self.configFile = configFile
        self.directory = directory
        self.configFilePath = path.join(directory, configFile)

    def read(self):
        """
        loads config object from file.
        """

        configFilePath = self.configFilePath

        try:
            with open(configFilePath, "rb") as f:
                config = load(f)
            return config
        except EOFError:
            return Config()

    def write(self, config):
        """
        writes config object to file.
        """
        configFilePath = self.configFilePath
        with open(configFilePath, "wb") as f:
            dump(config, f)

