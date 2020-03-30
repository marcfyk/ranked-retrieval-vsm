from os import path

import os

class Document:
    """
    document object containing docId and the path to the file.
    """

    def __init__(self, docId, fileName, directory="", distance=0):
        """
        docId -> numeric id for document. (sorted based on docId)
        fileName -> file name.
        directory -> directory of file.
        distance -> euclidean distance of document vector wrt vector space model.
        """
        self.docId = docId
        self.fileName = fileName
        self.directory = directory
        self.filePath = path.join(directory, fileName)
        self.distance = distance

    @classmethod
    def parseFile(cls, fileName, directory=""):
        """
        fileName -> name of file.
        directory -> directory of file.

        returns a Document object representing this file.
        """

        assert fileName.isnumeric(), ("document: \"{fileName}\" should be numeric")
        return Document(int(fileName), fileName, directory)

    @classmethod
    def parseDirectory(cls, directory, limit=-1):
        """
        directory -> directory of files to be parsed into Document objects.
        returns a sorted list of Document objects.
        """

        documentMap = {}
        documents = sorted([cls.parseFile(fileName, directory) for fileName in os.listdir(directory)])
        if limit > 0:
            documents = documents[:limit]
        for docId, document in [(d.docId, d) for d in documents]:
            documentMap[docId] = document
        return documentMap

    def read(self):
        """
        reads the data from the file.
        """
        filePath = self.filePath
        with open(filePath, "r") as f:
            data = f.read()
        return data

    def __str__(self):
        return f"{self.docId}"

    def __repr__(self):
        return f"id: {self.docId}, file path: \"{self.filePath}\", distance: {self.distance}"

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
