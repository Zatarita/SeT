from saber.file.saber_file_generic import SaberFileGeneric
from common.data_parsing import StreamParser, StreamWriter


class SaberPak(SaberFileGeneric):
    type_definitions = {
        "Scene Data": 0,
        "Data": 1,
        "Single Player Lines": 2,
        "Shader": 3,
        "Textures Info": 5,
        "Sound Data": 8,
        "Memory": 10,
        "Skull Data": 11,
        "Template": 12,
        "String List": 14,
        "Game Logic": 16,
        "Breakable glass": 17,
        "Effects": 18,
        "(.grs)": 22,
        "Rain": 25,
        "(.cdt)": 26,
        "(.sm)": 27,
        "(.vis)": 29,
        "Animation Stream Data": 30
    }

    class Child:
        def __init__(self, stream=None):
            if stream:
                self.loadFromStream(stream)
                return

            self.offset = 0
            self.size = 0
            self.string_length = 0
            self.string = ""
            self.type = 0

            self.data = None

        def loadFromStream(self, stream):
            self.offset = stream.readInt(4)
            self.size = stream.readInt(4)
            self.string_length = stream.readInt(4)
            self.string = stream.readString(encoding="utf-8", length=self.string_length)
            self.type = stream.readInt(4)
            stream.burn(8)

            # if the name is blank, it's SceneData
            self.string = "SceneData" if not self.string else self.string

        def loadFromRawData(self, data):
            stream = StreamParser(data)
            self.loadFromStream(stream)

        def loadFromFile(self, path, file_type):
            with open(path, "rb") as file:
                self.data = file.read()

            # set offset to -1 so we can check if offsets dirty later
            self.offset = -1
            self.size = len(self.data)
            if ".tpl" in path:
                path = path.split(".")[0]
            self.string = path.split("/")[-1]
            self.string_length = len(self.string)
            self.type = file_type

        def parseOffset(self, stream):
            stream.seek(self.offset)
            self.data = stream.read(self.size)

        def formatData(self):
            output = StreamWriter()
            output.writeInt(self.offset)
            output.writeInt(self.size)
            # if scene data, don't write a string
            if self.string == "SceneData":
                output.writeInt(0)
            else:
                output.writeInt(self.string_length)
                output.writeString(self.string, encoding="utf-8")
            output.writeInt(self.type)
            # write padding
            output.write(b"\x00" * 8)
            return output.getvalue()

        def getData(self):
            return self.data

    def __init__(self):
        SaberFileGeneric.__init__(self)

    def parseData(self):
        data_stream = StreamParser(self.data)
        count = data_stream.readInt(4)

        for i in range(count):
            child = self.Child(data_stream)
            self.children.update({child.string: child})

        for child in self.children.values():
            child.parseOffset(data_stream)

    def recalculateOffsets(self):
        offset = 4

        # first pass to figure out the header size
        for child in self.children.values():
            # magic number: 24 = size of each entry.
            offset += child.string_length + 24

        # second pass set the offsets, and increment data size sequentially
        for child in self.children.values():
            child.offset = offset
            offset += len(child.data)

    def addEntry(self, path, data_type):
        child = self.Child()
        if type(data_type) != int:
            data_type = self.type_definitions.get(data_type, -1)
        if data_type not in list(self.type_definitions.values()):
            print("Unknown type")
            return
        child.loadFromFile(path, data_type)
        self.importChild(child.string, child)
        self.recalculateOffsets()

    # -----------------------------------------------------Compile Data Over Ride
    def compileData(self):
        stream = StreamWriter()
        stream.writeInt(len(self.children))
        self.recalculateOffsets()

        for child in self.children.values():
            stream.write(child.formatData())

        for child in self.children.values():
            stream.write(child.data)

        return stream.getvalue()
