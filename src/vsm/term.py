from .postingslistfilehandler import PostingsListFileHandler 

class Term:
    """
    contains the term, document frequency, the line number and pointer to the a given file that it is stored in.
    """
    
    def __init__(self, term, docFreq, postingsListFilePos):
        """
        term -> string.
        docFreq -> number of documents that the term is observed.
        postingsListFilePos -> file position of postings list file.
        """
        self.term = term
        self.docFreq = docFreq
        self.postingsListFilePos = postingsListFilePos

    def getPostingsList(self, postingsListFileHandler):
        """
        postingsListFileHandler -> file handler object to get postings list.

        if line number and pointer are both invalid, return None.
        else return by pointer if possible, else by line number.
        """
        pointer = self.postingsListFilePos.pointer
        lineNumber = self.postingsListFilePos.lineNumber
        hasValidLineNumber = lineNumber > -1
        hasValidPointer = pointer > -1
        if not hasValidLineNumber and not hasValidPointer:
            return
        if hasValidPointer:
            return self.getPostingsListByPointer(postingsListFileHandler)
        return self.getPostingsListByLineNumber(postingsListFileHandler)

    def getPostingsListByLineNumber(self, postingsListFileHandler):
        """
        postingsListFileHandler -> file handler object to get postings list.

        gets postings list via line number.
        """
        lineNumber = self.postingsListFilePos.lineNumber
        return postingsListFileHandler.getPostingsListByLineNumber(lineNumber)

    def getPostingsListByPointer(self, postingsListFileHandler):
        """
        postingsListFileHandler -> file handler object to get postings list.

        gets postings list via pointer.
        """
        pointer = self.postingsListFilePos.pointer
        return postingsListFileHandler.getPostingsListByPointer(pointer)

    def __repr__(self):
        return f"<term: {self.term}, doc freq: {self.docFreq}, postings list pos: {self.postingsListFilePos}>"

    def __hash__(self):
        return hash(self.term)

    def __eq__(self, o):
        return type(o) == Term and self.term == o.term
