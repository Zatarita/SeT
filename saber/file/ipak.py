from saber.file.saber_file_generic import SaberFileGeneric
from saber.file.imeta import Imeta
from common.data_parsing import StreamParser, StreamWriter


class Ipak(SaberFileGeneric):
    type_definitions = {
        0: "ARGB8888",
        10: "AI88",
        12: "OXT1",
        13: "AXT1",
        15: "XT3",
        17: "XT5",
        22: "XRGB8888",
        36: "DXN",
        37: "XT5A"
    }

    class Child:
        def __init__(self, stream=None, offset=0, size=0):
            if stream:
                self.loadFromStream(stream, offset, size)
                return

            self.width = 0
            self.height = 0
            self.face_count = 0
            self.type = 0
            self.mip_map_count = 0

            self.data = None

        def loadFromStream(self, stream, offset=0, size=0):
            stream.seek(offset)
            # 16 bytes of engine parser specifics
            stream.burn(16)
            self.width = stream.readInt(4)
            self.height = stream.readInt(4)
            stream.burn(4)
            self.face_count = stream.readInt(4)
            stream.burn(6)
            self.type = stream.readInt(4)
            # 6 bytes of engine parser specifics
            stream.read(6)
            self.mip_map_count = stream.readInt(4)
            # 6 bytes of engine parser specifics
            stream.read(6)

            # rest header-less dds
            self.data = stream.read(size)

        def loadFromFile(self, file, size):
            # to - do
            pass

        def formatData(self):
            output = StreamWriter()

            # don't worry about it. it doesn't need explanation
            output.write(b"\xf0\x00\xff\xff\xff\xff\x54\x43\x49\x50\x02\x01\xff\xff\xff\xff")
            output.writeInt(self.width)
            output.writeInt(self.height)
            output.writeInt(1)
            output.writeInt(self.face_count)
            output.write(b"\xf2\x00\xff\xff\xff\xff")
            output.writeInt(self.type)
            output.write(b"\xf9\x00\xff\xff\xff\xff")
            output.writeInt(self.mip_map_count)
            output.write(b"\xff\x00\xff\xff\xff\xff")
            output.write(self.data)
            output.write(b"\x01\x00\xff\xff\xff\xff")

            return output.getvalue()

        def getData(self):
            return self.formatData

        def getRawData(self):
            return self.data

    def __init__(self):
        SaberFileGeneric.__init__(self)
        self.imeta = Imeta()

    def parseData(self):
        data_stream = StreamParser(self.data)
        count = data_stream.readInt(4)

        self.imeta.data = self.data[0:0x290008]
        self.imeta.parseData()

        for entry in self.imeta.children.values():
            new_child = self.Child(data_stream, entry.offset, entry.size)
            self.children.update({entry.string: new_child})

    # -----------------------------------------------------Compile Data Over Ride
    def compileData(self):
        stream = StreamWriter()
        stream.write(self.imeta.compileData())

        for child in self.children.values():
            stream.write(child.formatData())
        stream.write(b'\0' * 0x200000)

        return stream.getvalue()
