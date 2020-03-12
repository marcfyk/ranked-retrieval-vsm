import re

"""
contains docID and term frequency.
"""
class Posting:
    pattern = re.compile("^[<][0-9]*[,][0-9]*[>]$")
    
    """
    docId -> docId of document.
    termFreq -> frequency of a term in this docId.
    """
    def __init__(self, docId, termFreq):
        self.docId = docId
        self.termFreq = termFreq

    @classmethod
    def parse(cls, postingLine):
        pattern = cls.pattern
        if not pattern.match(postingLine):
            return
        docId, termFreq = [int(x) for x in postingLine[1:-1].split(",")]
        return Posting(docId, termFreq)

    def __repr__(self):
        return f"<{self.docId},{self.termFreq}>"


