from argparse import ArgumentParser
from os import path
from sys import argv
from sys import exit

from os import path
from vsm import Config
from vsm import ConfigFileHandler
from vsm import VectorSpaceModel

import os

def usageMessage():
    return f"usage: {argv[0]} -c config-file-path"

parser = ArgumentParser()
parser.add_argument("-c", "--config", help=usageMessage(), required=True)
parser.add_argument("-d1", "--document", help=usageMessage(), required=False)
parser.add_argument("-d2", "--dictionary", help=usageMessage(), required=False)
parser.add_argument("-p", "--posting", help=usageMessage(), required=False)
args = parser.parse_args()

if not args.config:
    print(usageMessage())
    exit(2)

configFilePath = args.config
documentFilePath = args.document if args.document else "document.txt"
dictionaryFilePath = args.dictionary if args.dictionary else "dictionary.txt"
postingFilePath = args.posting if args.posting else "posting.txt"

config = Config(dictionaryFilePath, postingFilePath, documentFilePath)
ConfigFileHandler(configFilePath).write(config)

vectorSpaceModel = VectorSpaceModel(config)

exitCommand = "exit()"
i = input(f"input query here, type {exitCommand} to quit:\n")
while i != exitCommand:
    docs = vectorSpaceModel.rank(i)
    for i in range(len(docs)):
        print(f"{i + 1}: {docs[i]}")
    i = input(f"input query here, type {exitCommand} to quit:\n")