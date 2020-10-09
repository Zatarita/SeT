from saber.file.saber_file_generic import SaberFileGeneric
from common.data_parsing import StreamParser, StreamWriter


class Imeta(SaberFileGeneric):
    type_definitions = {
        0x30: "AI88",  # No block compression
        0x46: "AXT1/OXT1",  # BC1
        0x49: "XT3",  # BC2
        0x4c: "XT5",  # BC3
        0x4f: "XT5A",  # BC4
        0x52: "DXN",  # BC5
        0x5a: "ARGB8888/XRGB8888"  # No block compression
    }

    class Child:
        def __init__(self, stream=None):
            if stream:
                self.loadFromStream(stream)
                return

            self.string = ""
            self.width = 0
            self.height = 0
            self.mip_map_count = 0
            self.face_count = 0
            self.type = 0
            self.size = 0
            self.size2 = 0
            self.offset = 0
            self.size3 = 0

        def loadFromStream(self, stream):
            self.string = stream.readString(encoding="utf-8", length=0x108).rstrip("\0")
            stream.burn(4)
            self.width = stream.readInt(4)
            self.height = stream.readInt(4)
            stream.burn(4)
            self.mip_map_count = stream.readInt(4)
            self.face_count = stream.readInt(4)
            self.type = stream.readInt(4)
            stream.burn(8)
            self.size = stream.readInt(4)
            stream.burn(4)
            self.size2 = stream.readInt(4)
            self.offset = stream.readInt(4)
            stream.burn(4)
            self.size3 = stream.readInt(4)
            stream.burn(4)

        def loadFromFile(self, file):
            stream = StreamParser(open(file, "rb").read())
            self.loadFromStream(stream)
            pass

        def typeFromIpakChild(self, ipak_child):
            mapper = {
                "0": 0x5a,
                "10": 0x30,
                "12": 0x46,
                "13": 0x46,
                "15": 0x49,
                "17": 0x4c,
                "22": 0x5a,
                "36": 0x52,
                "37": 0x4f
            }
            self.type = mapper.get(str(ipak_child.type))

        def formatData(self):
            output = StreamWriter()
            output.writeString(self.string.ljust(0x108, "\0"))
            output.writeInt(1)
            output.writeInt(self.width)
            output.writeInt(self.height)
            output.writeInt(1)
            output.writeInt(self.mip_map_count)
            output.writeInt(self.face_count)
            output.writeInt(self.type)
            output.write(b'\0' * 8)
            output.writeInt(self.size)
            output.writeInt(0)
            output.writeInt(self.size2)
            output.writeInt(self.offset)
            output.writeInt(0)
            output.writeInt(self.size3)
            output.writeInt(0)
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

    def addEntry(self, path,):
        name = path.split("/")[-1].split(".")[0]
        if name in self.children.keys():
            self.children[name].loadFromFile(path)
        else:
            child = self.Child()
            child.loadFromFile(path)
            self.importChild(child.string, child)


    # -----------------------------------------------------Compile Data Over Ride
    def compileData(self):
        stream = StreamWriter()
        stream.writeInt(len(self.children))
        stream.writeInt(0)

        for child in self.children.values():
            stream.write(child.formatData())

        stream.write(b'\0' * (0x290008 - stream.tell()))

        return stream.getvalue()
