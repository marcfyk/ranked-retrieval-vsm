from os import path

from vsm import Config
from vsm import ConfigFileHandler
from vsm import Document
from vsm import Indexer

import os

configDir = "config"
configFile = "config.txt"
configFilePath = path.join(configDir, configFile)

dataDir = "data"
dictionaryFilePath = path.join(dataDir, "dictionary.txt")
postingsFilePath = path.join(dataDir, "postings.txt")
documentMapFilePath = path.join(dataDir, "documentMap.txt")

trainingDataDir = "training"

if not path.exists(dataDir):
    os.mkdir(dataDir)

if not path.exists(configDir):
    os.mkdir(configDir)

open(dictionaryFilePath, "w").close()
open(postingsFilePath, "w").close()
open(documentMapFilePath, "w").close()

config = Config(
        dictionaryFilePath=dictionaryFilePath, 
        postingsFilePath=postingsFilePath, 
        documentMapFilePath=documentMapFilePath)

documentMap = Document.parseDirectory(trainingDataDir, limit=20)

indexer = Indexer(config, step=1, documentMap=documentMap)
indexer.index()

configFileHandler = ConfigFileHandler(configFile, directory=configDir)
configFileHandler.write(config)

assert configFileHandler.read() == config, (f"config's integrity should be maintained, {config.dictionaryFilePath}, {config.postingsFilePath}, {config.documentMapFilePath}")

