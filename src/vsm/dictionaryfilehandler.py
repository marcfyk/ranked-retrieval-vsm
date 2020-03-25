from os import path
from pickle import load
from pickle import dump

class DictionaryFileHandler:
    """
    file handler to handle io operations for dictionary
    """

    def __init__(self, dictionaryFile, directory=""):
        """
        dictionaryFile -> file for dictionary to be read and written from.
        directory -> directory where dictionary file is in.
        """
        self.dictionaryFile = dictionaryFile
        self.directory = directory
        self.dictionaryFilePath = path.join(directory, dictionaryFile)

    def read(self):
        """
        reads dictionary from file.
        """

        dictionaryFilePath = self.dictionaryFilePath

        try:
            with open(dictionaryFilePath, "rb") as f:
                dictionary = load(f)
            return dictionary
        except EOFError:
            return {}

    def write(self, dictionary):
        """
        writes dictionary to file.
        """
        dictionaryFilePath = self.dictionaryFilePath
        with open(dictionaryFilePath, "wb") as f:
            dump(dictionary, f)

