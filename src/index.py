from argparse import ArgumentParser
from os import path
from sys import argv
from sys import exit

from vsm import Config
from vsm import ConfigFileHandler
from vsm import Document
from vsm import Indexer

import os

def usageMessage():
    return f"usage: {argv[0]} -c config-file-path -t training-directory"

def initializeFilePaths(*paths):
    for directory, fname in [path.split(p) for p in paths]:
        if directory and not path.exists(directory):
            os.mkdir(directory)
        open(fname, "w").close()

parser = ArgumentParser()
parser.add_argument("-c", "--config", help=usageMessage(), required=True)
parser.add_argument("-t", "--training", help=usageMessage(), required=True)
parser.add_argument("-d1", "--document", help=usageMessage(), required=False)
parser.add_argument("-d2", "--dictionary", help=usageMessage(), required=False)
parser.add_argument("-p", "--posting", help=usageMessage(), required=False)
args = parser.parse_args()

if not args.config or not args.training or not path.isdir(args.training):
    print(usageMessage())
    exit(2)

configFilePath = args.config
trainingDir = args.training
documentFilePath = args.document if args.document else "document.txt"
dictionaryFilePath = args.dictionary if args.dictionary else "dictionary.txt"
postingFilePath = args.posting if args.posting else "posting.txt"

initializeFilePaths(configFilePath, documentFilePath, dictionaryFilePath, postingFilePath)

config = Config(dictionaryFilePath=dictionaryFilePath, postingsFilePath=postingFilePath, documentMapFilePath=documentFilePath)
ConfigFileHandler(configFilePath).write(config)

documents = Document.parseDirectory(trainingDir)

indexer = Indexer(config, step=10000, documentMap=documents)
indexer.index()

