from collections import deque
from os import path

from .PostingsList import PostingsList

import os

"""
file handler to handle io operations for postings lists
"""
class PostingsListFileHandler:

    """
    postingsFile -> file for postings lists to be read and written from.
    directory -> directory where postings file is in.
    """
    def __init__(self, postingsFile, directory=""):
        self.postingsFile = postingsFile
        self.directory = directory
        self.postingsFilePath = path.join(directory, postingsFile)

    """
    reads postings list from a line number (zero-based)
    """
    def getPostingsListByLineNumber(self, lineNumber):
        # line number is zero based
        postingsFilePath = self.postingsFilePath
        with open(postingsFilePath, "r") as f:
            for i in range(0, lineNumber):
                line = f.readline()
        return PostingsList.parse(line)

    """
    reads postings list from a pointer (f.seek())
    """
    def getPostingsListByPointer(self, pointer):
        postingsFilePath = self.postingsFilePath
        with open(postingsFilePath, "r") as f:
            f.seek(pointer)
            line = f.readline()
        return PostingsList.parse(line)
    
    """
    termsAndPostings -> list of (Term object, list of Posting objects to be added)
    updates and/or adds postings list to file.
    """
    def writePostingsListsToMultipleLines(self, termsAndPostings):
        # termsAndPostings -> list of items where item = (Term obj, list of Posting objs)
        directory = self.directory
        postingsFilePath = self.postingsFilePath

        data = [(term.lineNumber, listOfPostings) for term, listOfPostings in termsAndPostings.items()] # map (Term, [postings]) -> (line number, [postings])
        sortedDataQueue = deque(sorted(data, key=lambda k : k[0])) # sorts data into a queue according to line number

        tempPostingsFilePath = path.join(directory, "temp-postings-file.txt")

        with open(postingsFilePath, "r") as f, open(tempPostingsFilePath, "w+") as t:

            nextLineNumber, nextListOfPostings = sortedDataQueue.popleft() if len(sortedDataQueue) else (-1, [])
            currentLine = 0

            # copys over existing lines in f to t, while updating lines that have updated values
            for line in f:
                if currentLine == nextLineNumber: # indicates that the line needs to be updated
                    postingsList = PostingsList.parse(line.strip())
                    postingsList.addAll(nextListOfPostings)
                    t.write(str(postingsList) + "\n")
                    nextLineNumber, nextListOfPostings = sortedDataQueue.popleft() if len(sortedDataQueue) else (-1, [])
                else: # indicates that the line has no update
                    t.write(line)
                currentLine += 1

            while nextLineNumber != -1: # resolves lines to be added that were not in f before
                assert nextLineNumber == currentLine, (f"next line number: {nextLineNumber}, current line: {currentLine}, next line number should == current line")
                postingsList = PostingsList(nextListOfPostings)
                t.write(str(postingsList) + "\n")
                nextLineNumber, nextListOfPostings = sortedDataQueue.popleft() if len(sortedDataQueue) else (-1, [])
                currentLine += 1

        os.replace(tempPostingsFilePath, postingsFilePath) # writes t to f

    """
    gets the pointer value for each start of a line in the file.
    """
    def fetchAllPointersToStartOfEachLine(self):
        postingsFilePath = self.postingsFilePath
        pointers = []
        with open(postingsFilePath, "r") as f:
            line = f.readline()
            while line:
                pointers.append(f.tell())
                line = f.readline()
        return pointers

    def __repr__(self):
       return f"file handle path: {self.postingsFilePath}"

