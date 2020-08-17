from abc import ABCMeta, abstractmethod
from compression.h1a.decompress import decompressor

"""
    FileGeneric:
        Handles the compression and I/O of raw data.
"""


class FileGeneric(metaclass=ABCMeta):
    def __init__(self):
        self.compressed = False
        self.data = None

    # compress the file data
    def compress(self):
        # if self.compressed:
        # self.compressed = False
        pass

    # decompress the files data
    def decompress(self):
        self.data = decompressor(self.data)
        pass

    # Load a file from path.
    def load(self, path, compressed=False):
        # Read the file contents
        with open(path, "rb") as file:
            self.data = file.read()

        # Decompress if compressed
        if compressed:
            self.decompress()

    # Save a file to path.
    def save(self, path):
        # Compress if it was originally compressed
        if not self.compressed:
            self.compress()

        # Format the data
        self.data = self.compileData()

        # Save
        with open(path, "wb") as file:
            file.write(self.data)

    # -----------------------------------------------------Virtual Function **MUST OVERRIDE**
    @abstractmethod
    def compileData(self):
        pass

