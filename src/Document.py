
"""
document object containing docId and the path to the file.
"""
class Document:

    """
    docId -> numeric id for document. (sorted based on docId)
    filePath -> file path to document.
    """
    def __init__(self, docId, filePath):
        self.docId = docId
        self.filePath = filePath

    def __repr__(self):
        return f"ID: {self.docId}, file path: {self.filePath}"

    def __lt__(self, o):
        return type(o) == Document and self.docId < o.docId

    def __le__(self, o):
        return stype(o) == Document and self.docId <= o.docId

    def __gt__(self, o):
        return stype(o) == Document and self.docId > o.docId

    def __ge__(self, o):
        return stype(o) == Document and self.docId >= o.docId

    def __eq__(self, o):
        return stype(o) == Document and self.docId == o.docId

    def __ne__(self, o):
        return stype(o) == Document and self.docId != o.docId

