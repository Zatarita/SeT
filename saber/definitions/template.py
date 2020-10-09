from common.data_parsing import StreamParser
from saber.file.imeta import Imeta


class Template:
    def __init__(self, data):
        self.data = data
        stream = StreamParser(data)

        self.dependecies = []

        # for now, this will do for gathering the dependencies
        stream.burn(8)
        header_size = stream.readInt(4)
        stream.burn(4)
        self.name = stream.readString()
        stream.seek(header_size)
        stream.burn(15)
        dependency_count = stream.readInt(4)
        stream.burn(6)
        for i in range(dependency_count):
            self.dependecies.append(stream.readString())
            stream.burn(6)

    def extractRecursive(self, imeta: Imeta(), path):
        for dependency in self.dependecies:
            imeta.exportChild(path + "/" + dependency + ".imeta_child", dependency)
        open(path + "/" + self.name, "wb").write(self.data)
