from math import log
from os import path

from nltk.stem import PorterStemmer

from .dictionaryfilehandler import DictionaryFileHandler
from .documentmapfilehandler import DocumentMapFileHandler
from .postingslistfilehandler import PostingsListFileHandler
from .score import Score
from .scoremaxheap import ScoreMaxHeap


class VectorSpaceModel:
    """
    Represents the vector space model, facilitating ranking of queries.
    """

    def __init__(self, config, stemmer=None):
        """
        dictionaryFileHandler -> file handler for dictionary.
        postingsListFileHandler -> file handler for postings lists.
        documentMapFileHandler -> file handler for document map.
        stemmer -> stemmer for queries.

        dictionary -> dictionary of terms (term string -> term object)
        documentMap -> dictionary of documents (docId -> document object)

        dictionary and documentMap are loaded from their file handlers.
        """

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
        """
        loads dictionary and document map from their file handlers.
        """
        dictionaryFileHandler = self.dictionaryFileHandler 
        documentMapFileHandler = self.documentMapFileHandler
        self.dictionary = dictionaryFileHandler.read()
        self.documentMap = documentMapFileHandler.read()

    def processQuery(self, query):
        """
        builds a dictionary histogram of terms in query. (stemming applied)
        """
        stem = self.stemmer.stem
        dictionary = self.dictionary

        terms = [stem(t.strip().casefold()) for t in query.strip().split(" ")]
        filteredTerms = [dictionary[t] for t in terms if t in dictionary]
        queryTerms = {}
        for term in filteredTerms:
            if term not in queryTerms:
                queryTerms[term] = 0
            queryTerms[term] += 1
        return queryTerms
    
    def rank(self, query, limit=10):
        """
        sends a sorted list of documents ranked by their cosine score.
        """
        documentMap = self.documentMap
        postingsListFileHandler = self.postingsListFileHandler

        tf = lambda f : 1 + log(f, 10)
        idf = lambda n, f : log(n / f, 10)

        N = len(documentMap)
        scores = {}

        queryTerms = self.processQuery(query)
        queryWeights = [tf(freq) * idf(N, term.docFreq) for term, freq in queryTerms.items()]

        for queryTerm, queryWeight in zip(queryTerms, queryWeights):
            for posting in queryTerm.getPostingsList(postingsListFileHandler):
                docId, termFreq = posting.docId, posting.termFreq
                docWeight = tf(termFreq)
                if docId not in scores:
                    scores[docId] = Score(documentMap[docId], 0)
                scores[docId] += Score(documentMap[docId], queryWeight * docWeight)

        normalizedScores = [score / score.doc.distance for score in scores.values()]
        scoreHeap = ScoreMaxHeap.heapify(normalizedScores)

        result = [scoreHeap.pop().doc for i in range(min(limit, len(scoreHeap)))]

        return result

