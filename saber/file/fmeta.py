from saber.file.saber_file_generic import SaberFileGeneric
from common.data_parsing import StreamParser, StreamWriter

from compression.h1a.decompress import decompressor

class Fmeta(SaberFileGeneric):
    class Child:
        def __init__(self, stream=None):
            if stream:
                self.loadFromStream(stream)
                return

            self.string = ""
            self.type = 0
            self.decompressed_size = 0

        def loadFromStream(self, stream):
            self.string = stream.readString(encoding="utf-8", length=0x100).rstrip("\0")
            stream.burn(4)
            self.type = stream.readInt(4)
            self.decompressed_size = stream.readInt(4)
            stream.burn(4)

        def loadFromFile(self, file, size):
            self.string = file
            self.type = int(size != -1)
            self.decompressed_size = size

        def formatData(self):
            output = StreamWriter()
            output.writeString(self.string.ljust(0x100, "\0"))
            output.writeInt(0)
            output.writeInt(self.type)
            if self.type == 0:
                output.write(b'\xff' * 8)
            else:
                output.writeInt(self.decompressed_size)
                output.write(b'\00' * 4)
            return output.getvalue()

        def getData(self):
            return self.formatData()

    def __init__(self):
        SaberFileGeneric.__init__(self)

    def parseData(self):
        data_stream = StreamParser(self.data)
        count = data_stream.readInt(4)
        data_stream.burn(4)

        for i in range(count):
            new_child = self.Child(data_stream)
            self.children.update({new_child.string: new_child})

    def addEntry(self, file, size):
        child = self.Child()
        child.loadFromFile(file, size)
        self.importChild(child.string, child)

    def map_names(self):
        return [child.string for child in self.children.values() if child.type == 1]

    def s3dpak_names(self):
        return [child.string for child in self.children.values() if child.type == 0]

    # -----------------------------------------------------Compile Data Over Ride
    def compileData(self):
        stream = StreamWriter()
        stream.writeInt(len(self.children))

        for child in self.children.values():
            stream.write(child.formatData())

        stream.write(b'\0' * (0x4408 - stream.tell()))

        return stream.getvalue()

    @staticmethod
    def get_decompressed_size(path):
        with open(path, "rb") as file:
            content = file.read()
        map_data = decompressor(content)
        return len(map_data)