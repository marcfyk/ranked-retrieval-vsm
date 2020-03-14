from os import path

import os

"""
document object containing docId and the path to the file.
"""
class Document:

    """
    docId -> numeric id for document. (sorted based on docId)
    fileName -> file name.
    directory -> directory of file.
    """
    def __init__(self, docId, fileName, directory=""):
        self.docId = docId
        self.fileName = fileName
        self.directory = directory
        self.filePath = path.join(directory, fileName)

    """
    fileName -> name of file.
    directory -> directory of file.

    returns a Document object representing this file.
    """
    @classmethod
    def parseFile(cls, fileName, directory=""):
        assert fileName.isnumeric(), ("document: \"{fileName}\" should be numeric")
        return Document(int(fileName), fileName, directory)

    """
    directory -> directory of files to be parsed into Document objects.

    returns a sorted list of Document objects.
    """
    @classmethod
    def parseDirectory(cls, directory, limit=-1):
        documentMap = {}
        documents = sorted([cls.parseFile(fileName, directory) for fileName in os.listdir(directory)])
        if limit > 0:
            documents = documents[:limit]
        for docId, document in [(d.docId, d) for d in documents]:
            documentMap[docId] = document
        return documentMap

    def __repr__(self):
        return f"ID: {self.docId}, file path: \"{self.filePath}\""

    def __hash__(self):
        return hash(self.docId)

    def __lt__(self, o):
        return type(o) == Document and self.docId < o.docId

    def __le__(self, o):
        return type(o) == Document and self.docId <= o.docId

    def __gt__(self, o):
        return type(o) == Document and self.docId > o.docId

    def __ge__(self, o):
        return type(o) == Document and self.docId >= o.docId

    def __eq__(self, o):
        return type(o) == Document and self.docId == o.docId

    def __ne__(self, o):
        return type(o) == Document and self.docId != o.docId
