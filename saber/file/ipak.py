from saber.file.saber_file_generic import SaberFileGeneric
from saber.file.imeta import Imeta
from common.data_parsing import StreamParser, StreamWriter
from directx.header import DDS_TEXTURE


class Ipak(SaberFileGeneric):
    type_definitions = {
        0: "ARGB8888",
        10: "AI88",
        12: "OXT1", #
        13: "AXT1", #
        15: "XT3", #
        17: "XT5", #
        22: "XRGB8888",
        36: "DXN", #
        37: "XT5A" #
    }

    class Child:
        def __init__(self, stream=None, offset=0, size=0):
            if stream:
                self.loadFromStream(stream, offset, size)
                return

            self.width = 0
            self.height = 0
            self.face_count = 1
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

        def loadFromFile(self, file):
            dds = DDS_TEXTURE()
            dds.load(file)
            self.width = dds.header.width
            self.height = dds.header.height
            self.mip_map_count = dds.header.mipmap_count
            self.face_count = dds.getFaceCount()
            self.type = dds.typeToHaloEnum()
            self.data = dds.pixelData

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

    def __init__(self, path = None):
        SaberFileGeneric.__init__(self)
        self.imeta = Imeta()
        if path:
            self.load(path, True)
            self.parseData()

    def parseData(self):
        data_stream = StreamParser(self.data)
        count = data_stream.readInt(4)

        self.imeta.data = self.data[0:0x290008]
        self.imeta.parseData()

        for entry in self.imeta.children.values():
            new_child = self.Child(data_stream, entry.offset, entry.size)
            self.children.update({entry.string: new_child})

    def loadFromDDS(self, path):
        # create ipak child
        new_child = self.Child()
        new_child.loadFromFile(path)
        # create imeta entry from child
        new_imeta_child = Imeta.Child()
        new_imeta_child.string = path.split("/")[-1].split(".")[0]
        new_imeta_child.height = new_child.height
        new_imeta_child.width = new_child.width
        new_imeta_child.mip_map_count = new_child.mip_map_count
        new_imeta_child.face_count = new_child.face_count
        new_imeta_child.size = len(new_child.data)
        new_imeta_child.size2 = len(new_child.data)
        new_imeta_child.size3 = len(new_child.data)
        new_imeta_child.typeFromIpakChild(new_child)
        self.children.update({new_imeta_child.string: new_child})
        self.imeta.children.update({new_imeta_child.string: new_imeta_child})

    # -----------------------------------------------------Compile Data Over Ride
    def compileData(self):
        stream = StreamWriter()

        offset = 0x290008
        names = self.imeta.names()
        for i in range(len(self.children)):
            self.imeta.children[names[i]].offset = offset
            offset += len(self.children[names[i]].data) + 64

        stream.write(self.imeta.compileData())

        for child in self.children.values():
            stream.write(child.formatData())
        stream.write(b'\0' * 0x200000)

        return stream.getvalue()
