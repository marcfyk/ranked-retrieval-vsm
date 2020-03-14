from math import log
from os import path

from nltk.stem import PorterStemmer

from .DictionaryFileHandler import DictionaryFileHandler
from .DocumentMapFileHandler import DocumentMapFileHandler
from .PostingsListFileHandler import PostingsListFileHandler


class VectorSpaceModel:

    def __init__(self, config, stemmer=None):

        dictionaryDir, dictionaryFile = path.split(config.dictionaryFilePath)
        postingsDir, postingsFile = path.split(config.postingsFilePath)
        documentMapDir, documentMapFile = path.split(config.documentMapFilePath)

        self.dictionaryFileHandler = DictionaryFileHandler(dictionaryFile, directory=dictionaryDir)
        self.postingsListFileHandler = PostingsListFileHandler(postingsFile, directory=postingsDir)
        self.documentMapFileHandler = DocumentMapFileHandler(documentMapFile, directory=documentMapDir)
        self.stemmer = PorterStemmer() if stemmer is None else stemmer

        self.dictionary = {}
        self.documentMap = {}
        self.setUp()

    def setUp(self):
        dictionaryFileHandler = self.dictionaryFileHandler 
        documentMapFileHandler = self.documentMapFileHandler
        self.dictionary = dictionaryFileHandler.read()
        self.documentMap = documentMapFileHandler.read()

    def buildQueryVector(self, line):
        stemmer = self.stemmer
        dictionary = self.dictionary
        documentMap = self.documentMap
        postingsListFileHandler = self.postingsListFileHandler

        N = len(documentMap)
        terms = [stemmer.stem(t) for t in line.split(" ")]
        scores = [0 for i in range(N)]
        length = [0 for i in range(N)]
        print(terms) 
        











