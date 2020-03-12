from .PostingsListFileHandler import PostingsListFileHandler 

"""
contains the term, document frequency, the line number and pointer to the a given file that it is stored in.
"""
class Term:
    
    """
    term -> string.
    docFreq -> number of documents that the term is observed.
    lineNumber -> line number of postings list of this term in file.
    pointer -> pointer of postings list of this term in file.
    """
    def __init__(self, term, docFreq, lineNumber=-1, pointer=-1):
        self.term = term
        self.docFreq = docFreq
        self.lineNumber = lineNumber
        self.pointer = pointer

    """
    postingsListFileHandler -> file handler object to get postings list.

    if line number and pointer are both invalid, return None.
    else return by pointer if possible, else by line number.
    """
    def getPostingsList(self, postingsListFileHandler):
        pointer = self.pointer
        lineNumber = self.lineNumber
        hasValidLineNumber = lineNumber > -1
        hasValidPointer = pointer > -1
        if not hasValidLineNumber and not hasValidPointer:
            return
        if hasValidPointer:
            return self.getPostingsListByPointer(postingsListFileHandler)
        return getPostingsListByLineNumber(postingsListFileHandler)

    """
    postingsListFileHandler -> file handler object to get postings list.

    gets postings list via line number.
    """
    def getPostingsListByLineNumber(self, postingsListFileHandler):
        lineNumber = self.lineNumber
        return postingsListFileHandler.getPostingsListByLineNumber(lineNumber)

    """
    postingsListFileHandler -> file handler object to get postings list.

    gets postings list via pointer.
    """
    def getPostingsListByPointer(self, postingsListFileHandler):
        pointer = self.pointer
        return postingsListFileHandler.getPostingsListByPointer(pointer)

    def __repr__(self):
        return f"term: {self.term}, document frequency: {self.docFreq}, line number: {self.lineNumber}, pointer: {self.pointer}"

    def __hash__(self):
        return hash(self.term)

    def __eq__(self, o):
        return type(o) == Term and self.term == o.term
