from .PostingsListFileHandler import PostingsListFileHandler 

"""
contains the term, document frequency, the line number and pointer to the a given file that it is stored in.
"""
class Term:
    
    """
    term -> string.
    docFreq -> number of documents that the term is observed.
    postingsListFilePointer -> file position of postings list file.
    lineNumber -> line number of postings list of this term in file.
    pointer -> pointer of postings list of this term in file.
    """
    def __init__(self, term, docFreq, postingsListFilePos):
        self.term = term
        self.docFreq = docFreq
        self.postingsListFilePos = postingsListFilePos

    """
    postingsListFileHandler -> file handler object to get postings list.

    if line number and pointer are both invalid, return None.
    else return by pointer if possible, else by line number.
    """
    def getPostingsList(self, postingsListFileHandler):
        pointer = self.postingsListFilePos.pointer
        lineNumber = self.postingsListFilePos.lineNumber
        hasValidLineNumber = lineNumber > -1
        hasValidPointer = pointer > -1
        if not hasValidLineNumber and not hasValidPointer:
            return
        if hasValidPointer:
            return self.getPostingsListByPointer(postingsListFileHandler)
        return self.getPostingsListByLineNumber(postingsListFileHandler)

    """
    postingsListFileHandler -> file handler object to get postings list.

    gets postings list via line number.
    """
    def getPostingsListByLineNumber(self, postingsListFileHandler):
        lineNumber = self.postingsListFilePos.lineNumber
        return postingsListFileHandler.getPostingsListByLineNumber(lineNumber)

    """
    postingsListFileHandler -> file handler object to get postings list.

    gets postings list via pointer.
    """
    def getPostingsListByPointer(self, postingsListFileHandler):
        pointer = self.postingsListFilePos.pointer
        return postingsListFileHandler.getPostingsListByPointer(pointer)

    def __repr__(self):
        return f"<term: {self.term}, doc freq: {self.docFreq}, postings list pos: {self.postingsListFilePos}>"

    def __hash__(self):
        return hash(self.term)

    def __eq__(self, o):
        return type(o) == Term and self.term == o.term
