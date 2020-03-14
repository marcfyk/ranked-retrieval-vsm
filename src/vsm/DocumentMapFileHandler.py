from os import path
from pickle import load
from pickle import dump

class DocumentMapFileHandler:

    def __init__(self, documentMapFile, directory=""):
        self.documentMapFile = documentMapFile
        self.directory = directory
        self.documentMapFilePath = path.join(directory, documentMapFile)

    def read(self):
        documentMapFilePath = self.documentMapFilePath

        try:
            with open(documentMapFilePath, "rb") as f:
                documentMap = load(f)
            return documentMap
        except EOFError:
            return {}

    def write(self, documentMap):
        documentMapFilePath = self.documentMapFilePath
        with open(documentMapFilePath, "wb") as f:
            dump(documentMap, f)

