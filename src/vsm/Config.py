

class Config:

    """
    wraps file paths into config object.
    """
    def __init__(self, dictionaryFilePath="", postingsFilePath="", documentMapFilePath=""):
        self.dictionaryFilePath = dictionaryFilePath
        self.postingsFilePath = postingsFilePath
        self.documentMapFilePath = documentMapFilePath

    def __hash__(self):
        return hash(self.dictionaryFilePath, self.postingsFilePath, self.documentMapFilePath)

    def __eq__(self, o):
        checkDictionaryFilePath = self.dictionaryFilePath == o.dictionaryFilePath
        checkPostingsFilePath = self.postingsFilePath == o.postingsFilePath
        checkDocumentMapFilePath = self.documentMapFilePath == o.documentMapFilePath
        return checkDictionaryFilePath and checkPostingsFilePath and checkDocumentMapFilePath

    def __repr__(self):
        return f"dictionary -> {self.dictionaryFilePath}, postings -> {self.postingsFilePath}, documents -> {self.documentMapFilePath}"

