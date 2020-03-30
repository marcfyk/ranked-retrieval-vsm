from os import path
from pickle import load
from pickle import dump

class DocumentMapFileHandler:
    """
    file handler for document map.
    """

    def __init__(self, documentMapFile, directory=""):
        """
        documentMapFile -> file name.
        directory -> directory to store documentMap file.
        """
        self.documentMapFile = documentMapFile
        self.directory = directory
        self.documentMapFilePath = path.join(directory, documentMapFile)

    def read(self):
        """
        loads documentMap object from file.
        """
        documentMapFilePath = self.documentMapFilePath

        try:
            with open(documentMapFilePath, "rb") as f:
                documentMap = load(f)
            return documentMap
        except EOFError:
            return {}

    def write(self, documentMap):
        """
        writes documentMap object to file.
        """
        documentMapFilePath = self.documentMapFilePath
        with open(documentMapFilePath, "wb") as f:
            dump(documentMap, f)

