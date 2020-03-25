
class Score:
    """
    Score of a document.
    """

    def __init__(self, doc, score=0):
        """
        doc -> document object that the score belongs to.
        """
        self.doc = doc
        self.score = score

    def __add__(self, o):
        if type(o) == Score:
            return Score(self.doc, self.score + o.score)

        if type(o) == float or type(o) == int:
            return Score(self.doc, self.score + o)

        raise ValueError

    def __truediv__(self, o):
        if type(o) == Score:
            return Score(self.doc, self.score / o.score)

        if type(o) == float or type(o) == int:
            return Score(self.doc, self.score / o)

        return ValueError

    def __repr__(self):
        return str(f"docId: {self.doc.docId}, score: {self.score}")

    def __lt__(self, o):
        return self.score < o.score

    def __le__(self, o):
        return self.score <= o.score
    
    def __gt__(self, o):
        return self.score > o.score

    def __ge__(self, o):
        return self.score >= o.score

    def __eq__(self, o):
        return self.score == o.score

    def __ne__(self, o):
        return self.score != o.score
