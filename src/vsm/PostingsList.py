from .Posting import Posting

"""
list of postings, which contains docID and term frequency each.
"""
class PostingsList:
    delimiter = " "

    """
    postings -> list of Posting objects, default = []
    """
    def __init__(self, postings=[]):
        self.postings = [x for x in postings]

    """
    parses a given line into a PostingsList object.
    """
    @classmethod
    def parse(self, line):
        delimiter = PostingsList.delimiter
        postings = line.split(delimiter)
        return PostingsList([Posting.parse(posting) for posting in postings])

    """
    add one posting to list of postings
    """
    def add(self, posting):
        self.postings.append(posting)

    """
    add multiple postings to list of postings.
    """
    def addAll(self, postings):
        self.postings.extend(postings)

    def __repr__(self):
        delimiter = PostingsList.delimiter
        postings = self.postings
        return  delimiter.join([str(posting) for posting in postings])

