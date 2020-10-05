from abc import ABCMeta, abstractmethod
from compression.h1a.decompress import decompressor
from compression.h1a.compress import compressor

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
        return compressor(self.data)

    # decompress the files data
    def decompress(self):
        self.data = decompressor(self.data)

    # Load a file from path.
    def load(self, path, compressed=False):
        # Read the file contents
        with open(path, "rb") as file:
            self.data = file.read()

        # Decompress if compressed
        if compressed:
            self.decompress()
            self.compressed = True

    # Save a file to path.
    def save(self, path):
        # Format the data
        self.data = self.compileData()

        # Save
        with open(path, "wb") as file:
            file.write(self.data if not self.compressed else self.compress())

    # -----------------------------------------------------Virtual Function **MUST OVERRIDE**
    @abstractmethod
    def compileData(self):
        pass

