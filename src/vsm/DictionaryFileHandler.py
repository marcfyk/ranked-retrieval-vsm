from os import path
from pickle import load
from pickle import dump

"""
file handler to handle io operations for dictionary
"""
class DictionaryFileHandler:

    """
    dictionaryFile -> file for dictionary to be read and written from.
    directory -> directory where dictionary file is in.
    """
    def __init__(self, dictionaryFile, directory=""):
        self.dictionaryFile = dictionaryFile
        self.directory = directory
        self.dictionaryFilePath = path.join(directory, dictionaryFile)

    """
    reads dictionary from file. (via pickle)
    """
    def read(self):
        dictionaryFilePath = self.dictionaryFilePath

        try:
            with open(dictionaryFilePath, "rb") as f:
                dictionary = load(f)
            return dictionary
        except EOFError:
            return {}

    """
    writes dictionary to file. (via pickle)
    """
    def write(self, dictionary):
        dictionaryFilePath = self.dictionaryFilePath
        with open(dictionaryFilePath, "wb") as f:
            dump(dictionary, f)

