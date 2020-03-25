import re

class Posting:
    """
    contains docID and term frequency.
    """

    # regex pattern for parsing strings to postings.
    pattern = re.compile("^[<][0-9]*[,][0-9]*[>]$")
    
    def __init__(self, docId, termFreq):
        """
        docId -> docId of document.
        termFreq -> frequency of a term in this docId.
        """
        self.docId = docId
        self.termFreq = termFreq

    @classmethod
    def parse(cls, postingString):
        """
        parses a posting string into a Posting.
        """
        pattern = cls.pattern
        if not pattern.match(postingString):
            raise ValueError(f"invalid format: \"{postingString}\"")
        docId, termFreq = [int(x) for x in postingString[1:-1].split(",")]
        return Posting(docId, termFreq)

    def __repr__(self):
        return f"<{self.docId},{self.termFreq}>"


