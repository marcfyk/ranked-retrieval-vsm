from functools import reduce
from math import sqrt
from math import log
from os import path

from .dictionaryfilehandler import DictionaryFileHandler
from .documentmapfilehandler import DocumentMapFileHandler
from .posting import Posting
from .postingslistfilehandler import PostingsListFileHandler
from .fileposition import FilePosition
from .term import Term

from nltk.stem import PorterStemmer
from nltk import sent_tokenize
from nltk import word_tokenize

class Indexer:
    """
    indexer objects can index documents to a dictionary and write to dictionary and write the dictionary and postings lists to disk.
    """


    def __init__(self, config, step=1, stemmer=None, documentMap={}):
        """
        dictionaryFilePath -> file path to read and write dictionary, will be wrapped in DictionaryFileHandler object.
        postingsFilePath -> file to read and write postings lists, will be wrapped in PostingsListFileHandler object.
        step -> the step at which to read documents into memory before writing to file, default = 1.
        stemmer -> stemmer to stem terms, default = PorterStemmer (nltk).
        documentMap -> map of documents to be indexed, mapping document ids to document objects.
        dictionary -> map of terms in the dictionary, mapping term strings 
        """

        dictionaryDir, dictionaryFile = path.split(config.dictionaryFilePath)
        postingsDir, postingsFile = path.split(config.postingsFilePath)
        documentMapDir, documentMapFile = path.split(config.documentMapFilePath)

        self.dictionaryFileHandler = DictionaryFileHandler(dictionaryFile, directory=dictionaryDir)
        self.postingsListFileHandler = PostingsListFileHandler(postingsFile, directory=postingsDir)
        self.documentMapFileHandler = DocumentMapFileHandler(documentMapFile, directory=documentMapDir)

        self.step = step
        self.stemmer = PorterStemmer() if stemmer is None else stemmer
        self.documentMap = {}
        for docId, doc in documentMap.items():
            self.documentMap[docId] = doc
        self.dictionary = {} # key -> term (string), value -> Term object

    def index(self):
        """
        sorts documents by docId.
        indexes all documents by appropriate batches, updating dictionary and postings file.
        writes dictionary to file.
        """

        step = self.step
        dictionaryFileHandler = self.dictionaryFileHandler
        postingsListFileHandler = self.postingsListFileHandler
        documentMapFileHandler = self.documentMapFileHandler
        documentMap = self.documentMap
        dictionary = self.dictionary

        sortedDocuments = sorted(documentMap.values())

        batches = [sortedDocuments[i:i+step] for i in range(0, len(sortedDocuments), step)]
        indexedDocCount = 0
        for docBatch in batches: # write postings list and update dictionary batch by batch
            terms = self.getTermsFromDocumentBatch(docBatch, dictionary)
            postingsListFileHandler.writePostingsListsToMultipleLines(terms)
            indexedDocCount += len(docBatch)
            print(f"indexed {indexedDocCount} / {len(sortedDocuments)}", end="\r")

        termObjects = dictionary.values()
        pointers = postingsListFileHandler.fetchAllPointersToStartOfEachLine()
        assert len(pointers) == len(termObjects), (f"pointers count = {len(pointers)}, term count = {len(termObjects)}, pointers count should equal term count")
        assert reduce(lambda x, y : (y, x[0] < y and x[1]), [term.postingsListFilePos.lineNumber for term in termObjects], (-1, True))[1] == True, ("checks if line numbers are sorted")
        
        for term, pointer in zip(termObjects, pointers): # updates pointers to all postings lists for efficient disk seeks
            term.postingsListFilePos.pointer = pointer

        dictionaryFileHandler.write(dictionary) # writes dictionary to file
        documentMapFileHandler.write(documentMap) # writes documents to file

        assert dictionaryFileHandler.read() == dictionary, ("dictionary integrity should be maintained")
        assert documentMapFileHandler.read() == documentMap, ("document map integrity should be maintained")

    def getTermsFromDocument(self, document, dictionary):
        """
        gets the terms from document after stemming.
        updates dictionary.
        returns a dictionary of Term object -> term frequency 
        """

        stemmer = self.stemmer

        termsToBeAdded = {} # key -> term (string), value -> term frequency

        isValidTerm = lambda t : reduce(lambda x, y : x or y.isalnum(), t, False)

        # reads file, stems words, adds them to termsToBeAdded
        data = document.read()
        for sentence in sent_tokenize(data):
            for word in word_tokenize(sentence):
                term = stemmer.stem(word.strip().casefold())
                if not isValidTerm(term):
                    continue
                if term not in termsToBeAdded:
                    termsToBeAdded[term] = 0
                termsToBeAdded[term] += 1 # update term frequency in this doc

        # updates dictionary based on terms from document
        for t in termsToBeAdded:
            if t not in dictionary:
                postingsListFilePos = FilePosition(lineNumber=len(dictionary))
                dictionary[t] = Term(t, 0, postingsListFilePos)
            term = dictionary[t]
            term.docFreq += 1 # update doc frequency of term in dictionary

        outputTerms = {} # key -> Term (obj), value -> term frequency 
        for term, termFreq in termsToBeAdded.items():
            outputTerms[dictionary[term]] = termFreq

        # euclidean distance calculation
        tf = lambda f : 1 + log(f, 10)
        document.distance = sqrt(sum([tf(f) ** 2 for f in termsToBeAdded.values()]))

        return outputTerms

    def getTermsFromDocumentBatch(self, documentBatch, dictionary):
        """
        get the terms from all documents in batch.
        returns a dictionary of Term object -> list of Posting objects (to be added)
        """
     
        totalOutputTerms = {} # key -> Term (obj), value -> list of Posting objects
        for doc in documentBatch:
            docId = doc.docId
            outputTerms = self.getTermsFromDocument(doc, dictionary)

            for term, termFreq in outputTerms.items():
                if term not in totalOutputTerms:
                    totalOutputTerms[term] = []
                totalOutputTerms[term].append(Posting(docId, termFreq))

        return totalOutputTerms
