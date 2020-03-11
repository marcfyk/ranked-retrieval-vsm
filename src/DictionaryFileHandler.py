from pickle import load
from pickle import dump

"""
file handler to handle io operations for dictionary
"""
class DictionaryFileHandler:

    """
    dictionaryFile -> file for dictionary to be read and written from.
    """
    def __init__(self, dictionaryFile):
        self.dictionaryFile = dictionaryFile

    """
    reads dictionary from file. (via pickle)
    """
    def readDictionary(self):
        dictionaryFile = self.dictionaryFile
        with open(dictionaryFile, "rb") as f:
            dictionary = load(f)
        return dictionary

    """
    writes dictionary to file. (via pickle)
    """
    def writeDictionary(self, dictionary):
        dictionaryFile = self.dictionaryFile
        with open(dictionaryFile, "wb") as f:
            dump(dictionary, f)

