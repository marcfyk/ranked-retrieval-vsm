"""
contains docID and term frequency.
"""
class Posting:
    
    """
    docId -> docId of document.
    termFreq -> frequency of a term in this docId.
    """
    def __init__(self, docId, termFreq):
        self.docId = docId
        self.termFreq = termFreq

    def __repr__(self):
        return f"({self.docID}, {self.termFreq})"


