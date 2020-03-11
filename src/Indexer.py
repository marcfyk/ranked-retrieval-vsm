from DictionaryFileHandler import DictionaryFileHandler
from PostingsListFileHandler import PostingsListFileHandler
from Term import Term

from functools import reduce
from nltk.stem import PorterStemmer
from nltk import sent_tokenize
from nltk import word_tokenize

"""
indexer objects can index documents to a dictionary and write to dictionary and write the dictionary and postings lists to disk.
"""
class Indexer:

    """
    dictionaryFile -> file to read and write dictionary, will be wrapped in DictionaryFileHandler object.
    postingsFile -> file to read and write postings lists, will be wrapped in PostingsListFileHandler object.
    step -> the step at which to read documents into memory before writing to file, default = 1
    stemmer -> stemmer to stem terms, default = PorterStemmer (nltk)
    """
    def __init__(self, dictionaryFile, postingsFile, step=1, stemmer=None):
        self.dictionaryFileHandler = DictionaryFileHandler(dictionaryFile)
        self.postingsListFileHandler = PostingsListFileHandler(postingsFile)
        self.step = step
        self.stemmer = PorterStemmer() if stemmer is None else stemmer

    """
    documents -> list of Document objects.

    sorts documents by docId.
    indexes all documents by appropriate batches, updating dictionary and postings file.
    writes dictionary to file.
    """
    def index(self, documents):

        dictionaryFileHandler = self.dictionaryFileHandler
        postingsListFileHandler = self.postingsListFileHandler

        dictionary = {} # key -> term (string), value -> Term object

        sortedDocuments = sorted(documents)
        batches = [sortedDocuments[i:i+step] for i in range(0, len(sortedDocuments), step)]
        for docBatch in batches: # write postings list and update dictionary batch by batch
            terms = self.getTermsFromDocumentBatch(docBatch, dictionary)
            postingsListFileHandler.writePostingsListsToMultipleLines(terms)

        termObjects = dictionary.values()
        pointers = postingsListFileHandler.fetchAllPointersToStartOfEachLine()
        assert len(pointers) == len(termObjects) ("there should be a pointer for each postings list belonging to each term in dictionary")
        assert reduce(lambda x, y : (y, x[0] < y and x[1]), [term.lineNumber for term in termObjects], (-1, True))[1] == True ("checks if line numbers are sorted")
        
        for term, pointer in zip(termObjects, pointers): # updates pointers to all postings lists for efficient disk seeks
            term.pointer = pointer

        dictionaryFileHandler.writeDictionary(dictionary) # writes dictionary to file

    """
    gets the terms from document after stemming.
    updates dictionary.
    returns a dictionary of Term object -> term frequency 
    """
    def getTermsFromDocument(self, document, dictionary):
        stemmer = self.stemmer
        docId = document.docId
        filePath = document.filePath

        termsToBeAdded = {} # key -> term (string), value -> term frequency

        # reads file, stems words, adds them to termsToBeAdded
        with open(document.filePath, "r") as f:
            data = f.read()
            for sentence in sent_tokenize(data):
                for word in word_tokenize(sentence):
                    term = stemmer.stem(word)
                    if term not in termsTobeAdded:
                        termsToBeAdded[term] = 0
                    termsToBeAdded[term] += 1 # update term frequency in this doc

        # updates dictionary based on terms from document
        for t in termsToBeAdded:
            if t not in dictionary:
                dictionary[t] = Term(t, 0, len(dictionary))
            term = dictionary[t]
            term.docFreq += 1 # update doc frequency of term in dictionary

        outputTerms = {} # key -> Term (obj), value -> term frequency 
        for term, termFreq in termsToBeAdded:
            outputTerms[dictionary[term]] = termFreq

        return outputTerms

    """
    get the terms from all documents in batch.
    returns a dictionary of Term object -> list of Posting objects (to be added)
    """
    def getTermsFromDocumentBatch(self, documentBatch, dictionary):
        postingsFile = self.postingsFile
        
        totalOutputTerms = {} # key -> Term (obj), value -> list of Posting objects
        for doc in documentBatch:
            docId = doc.docId
            outputTerms = getTermsFromDocument(doc, dictionary)

            for term, termFreq in outputTerms.items():
                if term not in totalOutputTerms:
                    totalOutputTerms[term] = []
                totalOutputTerms[term].append(Posting(docId, termFreq))

        return totalOutputTerms



