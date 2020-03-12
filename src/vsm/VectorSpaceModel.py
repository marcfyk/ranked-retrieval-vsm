from .DictionaryFileHandler import DictionaryFileHandler
from .PostingsListFileHandler import PostingsListFileHandler

class VectorSpaceModel:

    def __init__(self, dictionaryFilePath, postingsFilePath):

        dictionaryDir, dictionaryFile = path.split(dictionaryFilePath)
        postingsDir, postingsFile = path.split(postingsFilePath)

        self.dictionaryFileHandler = DictionaryFileHandler(dictionaryFile, directory=dictionaryDir)
        self.postingsListFileHandler = PostingsListFileHandler(postingsFile, directory=postingsDir)

        dictionaryFromFile = self.dictionaryFileHandler.readDictionary()
        self.dictionary = {} if dictionaryFromFile is None else dictionaryFromFile


