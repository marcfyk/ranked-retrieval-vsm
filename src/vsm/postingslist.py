from .posting import Posting

class PostingsList:
    """
    list of postings, which contains docID and term frequency each.
    """
    delimiter = " "

    def __init__(self, postings=[]):
        """
        postings -> list of Posting objects, default = []
        """
        self.postings = [x for x in postings]

    @classmethod
    def parse(self, line):
        """
        parses a given line into a PostingsList object.
        """
        delimiter = PostingsList.delimiter
        postings = line.strip().split(delimiter)
        return PostingsList([Posting.parse(posting) for posting in postings])

    def add(self, posting):
        """
        add one posting to list of postings
        """
        self.postings.append(posting)

    def addAll(self, postings):
        """
        add multiple postings to list of postings.
        """
        self.postings.extend(postings)

    def __repr__(self):
        delimiter = PostingsList.delimiter
        postings = self.postings
        return  delimiter.join([str(posting) for posting in postings])

    def __iter__(self):
        postings = self.postings
        N = len(postings)
        for i in range(N):
            yield postings[i]
