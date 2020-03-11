from PostingsList import PostingsList
from collections import deque

import os

"""
file handler to handle io operations for postings lists
"""
class PostingsListFileHandler:

    """
    postingsFile -> file for postings lists to be read and written from.
    """
    def __init__(self, postingsFile):
        self.postingsFile = postingsFile

    """
    reads postings list from a line number (zero-based)
    """
    def getPostingsListByLineNumber(self, lineNumber):
        # line number is zero based
        postingsFile = self.postingsFile
        with open(postingsFile, "r+") as f:
            for i in range(0, lineNumber):
                line = f.readline()
        return PostingsList.parse(line)

    """
    reads postings list from a pointer (f.seek())
    """
    def getPostingsListByPointer(self, pointer):
        postingsFile = self.postingsFile
        with open(postingsFile, "r+") as f:
            f.seek(pointer)
            line = f.readline()
        return PostingsList.parse(line)
    
    """
    termsAndPostings -> list of (Term object, list of Posting objects to be added)
    updates and/or adds postings list to file.
    """
    def writePostingsListsToMultipleLines(self, termsAndPostings):
        # termsAndPostings -> list of items where item = (Term obj, list of Posting objs)
        postingsFile = self.postingsFile

        data = [(term.lineNumber, listOfPostings) for term, listOfPostings in termsAndPostings] # map (Term, [postings]) -> (line number, [postings])
        sortedDataQueue = deque(sorted(data, key=lambda k : k[0])) # sorts data into a queue according to line number

        tempPostingsFile = "temp-postings-file.txt"

        with open(postingsFile, "r+") as f, open(tempPostingsFile, "w+") as t:

            nextLineNumber, nextListOfPostings = sortedDataQueue.popleft()
            currentLine = 0

            # copys over existing lines in f to t, while updating lines that have updated values
            for line in f:
                if currentLine == nextLineNumber: # indicates that the line needs to be updated
                    postingsList = PostingsList.parse(line)
                    postingsList.addAll(nextListOfPostings)
                    t.write(str(postingsList))
                    nextLineNumber, nextListOfPostings = sortedDataQueue.popleft() if len(sortedDataQueue) else (-1, [])
                else: # indicates that the line has no update
                    t.write(line)
                currentLine += 1
            while len(sortedDataQueue): # resolves lines to be added that were not in f before
                assert nextLineNumber == currentLine ("next line number to be written should be equal to current line counter")
                postingsList = PostingsList(nextListOfPostings)
                t.write(str(postingsList))
                nextLineNumber, nextListOfPostings = sortedDataQueue.popleft()

        os.replace(tempPostingsFile, postingsFile) # writes t to f

    """
    gets the pointer value for each start of a line in the file.
    """
    def fetchAllPointersToStartOfEachLine(self):
        postingsFile = self.postingsFile
        pointers = []
        with open(postingsFile, "r+") as f:
            line = f.readline()
            while line:
                pointers.append(f.tell())
        return pointers

    def __repr__(self):
       return f"file handle: {self.postingsFile}"

