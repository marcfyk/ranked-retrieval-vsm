from collections import deque
from os import path

from .postingslist import PostingsList

import os

class PostingsListFileHandler:
    """
    file handler to handle io operations for postings lists
    """

    def __init__(self, postingsFile, directory=""):
        """
        postingsFile -> file for postings lists to be read and written from.
        directory -> directory where postings file is in.
        """
        self.postingsFile = postingsFile
        self.directory = directory
        self.postingsFilePath = path.join(directory, postingsFile)

    def getPostingsListByLineNumber(self, lineNumber):
        """
        reads postings list from a line number (zero-based)
        """
        # line number is zero based
        postingsFilePath = self.postingsFilePath
        with open(postingsFilePath, "r") as f:
            for i in range(0, lineNumber):
                line = f.readline()
        return PostingsList.parse(line)

    def getPostingsListByPointer(self, pointer):
        """
        reads postings list from a pointer (f.seek())
        """
        postingsFilePath = self.postingsFilePath
        with open(postingsFilePath, "r") as f:
            f.seek(pointer)
            line = f.readline()
        return PostingsList.parse(line)
    
    def writePostingsListsToMultipleLines(self, termsAndPostings):
        """
        termsAndPostings -> list of (Term object, list of Posting objects to be added)
        updates and/or adds postings list to file.
        """
        directory = self.directory
        postingsFilePath = self.postingsFilePath

        # map (Term, [postings]) -> (line number, [postings])
        data = [(term.postingsListFilePos.lineNumber, listOfPostings) for term, listOfPostings in termsAndPostings.items()]
        # sorts data into a queue according to line number
        sortedDataQueue = deque(sorted(data, key=lambda k : k[0]))

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

    def fetchAllPointersToStartOfEachLine(self):
        """
        gets the pointer value for each start of a line in the file.
        """
        postingsFilePath = self.postingsFilePath
        pointers = [0]
        with open(postingsFilePath, "r") as f:
            while f.readline():
                pointers.append(f.tell())
        if len(pointers) > 1: # discard pointer at the end of file.
            pointers.pop()
        return pointers

    def __repr__(self):
       return f"file handle path: {self.postingsFilePath}"

