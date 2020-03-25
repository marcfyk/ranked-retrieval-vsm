
class FilePosition:
    """
    represents position in a file, storing a line number (zero based) and pointer.
    """

    def __init__(self, lineNumber=-1, pointer=-1):
        self.lineNumber = lineNumber
        self.pointer = pointer

    def __repr__(self):
        return f"line: {self.lineNumber}, pointer: {self.pointer}"
