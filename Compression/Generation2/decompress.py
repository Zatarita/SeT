import zlib
import sys
from PyQt5.QtCore import QFileInfo

class h2a_compressed_data():
    name = ""
    data = None

    count = 0
    offsets = []
    sizes = []
    blocks = []

    def __init__(self, filepath):
        self.name = QFileInfo(filepath).baseName()

        with open(filepath, "rb") as file:
            self.data = file.read()

        self.find_data()

    def find_data(self):
        self.count = int.from_bytes(self.data[0:4], "little")
        for i in range(self.count):
            self.offsets.append(int.from_bytes(self.data[8 + 8*i: 12 + 8*i], "little"))
        self.offsets.append(len(self.data))

        for i in range(len(self.offsets) - 1):
            self.sizes.append(self.offsets[i+1] - self.offsets[i])
        self.offsets.pop()

        for i in range(self.count):
            self.blocks.append(self.data[self.offsets[i]:self.offsets[i] + self.sizes[i]])

    def decompress(self):
        with open(".TMP/" + self.name + "_decomp", "wb") as file:
            for block in self.blocks:
                file.write(zlib.decompress(block))

    def save(self, path):
        try:
            shutil.copyfile(".TMP/" + self.name + "_decomp", path)
        except:
            print("File has not been decompressed.")

