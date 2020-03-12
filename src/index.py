from os import path

from vsm import Indexer
from vsm import Document

import os

dictionaryFile = "dictionary.txt"
postingsFile = "postings.txt"
trainingDataDir = "training"
outputDataDir = "data"

dictionaryFilePath = path.join(outputDataDir, dictionaryFile)
postingsFilePath = path.join(outputDataDir, postingsFile)

if not path.exists(outputDataDir):
    path.mkdir(outputDataDir)

open(dictionaryFilePath, "w").close()
open(postingsFilePath, "w").close()


docs = Document.parseDirectory(trainingDataDir)[:100]

indexer = Indexer(dictionaryFilePath, postingsFilePath, step=1, totalDocuments=docs)
indexer.index()

