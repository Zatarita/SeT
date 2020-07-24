from Compression.Generation1.decompress import h1a_compressed_data

import io
from struct import pack

class ipak():
    count = 0
    items = {}

    data = None

    ipak_hex_type = {
    0x30 : "AI88", #No block compression
    0x46 : "AXT1/OXT1", #BC1
    0x49 : "XT3", #BC2
    0x4c : "XT5", #BC3
    0x4f : "XT5A", #BC4
    0x52 : "DXN", #BC5
    0x5a : "ARGB8888/XRGB8888" # No block compression
    }

    class imeta():
        class ipak_data():
            data_hex_type = {
            0  : "ARGB8888",
            10 : "AI88",
            12 : "OXT1",
            13 : "AXT1",
            15 : "XT3",
            17 : "XT5",
            22 : "XRGB8888",
            36 : "DXN",
            37 : "XT5A"
            }

            #empty item
            def __init__(self):
                self.width = 0
                self.height = 0
                self.unknown = 1
                self.face_count = 0
                self.mipmap_count = 0
                self.type = 0

                self.data = None

            def load_from_stream(self, stream):
                stream.read(16)
                self.width = int.from_bytes(stream.read(4), "little")
                self.height = int.from_bytes(stream.read(4), "little")
                self.unknown = int.from_bytes(stream.read(4), "little")
                self.face_count = int.from_bytes(stream.read(4), "little")
                stream.read(6)
                self.type = int.from_bytes(stream.read(4), "little")
                stream.read(6)
                self.mipmap_count = int.from_bytes(stream.read(4), "little")
                stream.read(6)

                self.data = stream.read()

            def save_rawdata(self, path):
                with open(path, "wb") as file:
                    file.write(self.data)

            def save(self, path):
                with open(path, "wb") as file:
                    file.write(self.compile_data_with_header())

            def compile_data_with_header(self):
                output = io.BytesIO()

                output.write(b"\xf0\x00\xff\xff\xff\xff\x54\x43\x49\x50\x02\x01\xff\xff\xff\xff")
                output.write(pack("<i", self.width))
                output.write(pack("<i", self.height))
                output.write(pack("<i", self.unknown))
                output.write(pack("<i", self.face_count))
                output.write(b"\xf2\x00\xff\xff\xff\xff")
                output.write(pack("<i", self.type))
                output.write(b"\xf9\x00\xff\xff\xff\xff")
                output.write(pack("<i", self.mipmap_count))
                output.write(b"\xff\x00\xff\xff\xff\xff")
                output.write(self.data)
                output.write(b"\x01\x00\xff\xff\xff\xff")

                return output.getvalue()

        #empty item
        def __init__(self):
            self.string = ""
            self.constant1 = 1
            self.width = 0
            self.height = 0
            self.constant2 = 1
            self.mipmap_count = 0
            self.face_count = 0
            self.type = 0
            self.size = 0
            self.size2 = 0
            self.size3 = 0
            self.offset = 0

            self.data = None

        #load item from stream
        def load_from_stream(self, stream):
            self.string = stream.read(0x108).decode("utf-8").rstrip('\0')
            self.constant1 = int.from_bytes(stream.read(4), "little")
            self.width = int.from_bytes(stream.read(4), "little")
            self.height = int.from_bytes(stream.read(4), "little")
            self.constant2 = int.from_bytes(stream.read(4), "little")
            self.mipmap_count = int.from_bytes(stream.read(4), "little")
            self.face_count = int.from_bytes(stream.read(4), "little")
            self.type = int.from_bytes(stream.read(4), "little")
            stream.read(8)
            self.size = int.from_bytes(stream.read(4), "little")
            stream.read(4)
            self.size2 = int.from_bytes(stream.read(4), "little")
            self.offset = int.from_bytes(stream.read(4), "little")
            stream.read(4)
            self.size3 = int.from_bytes(stream.read(4), "little")
            stream.read(4)

        def parse_block_data(self, stream):
            self.data = self.ipak_data()
            self.data.load_from_stream(stream)

        #generate imeta entries
        def compile_data(self):
            output = io.BytesIO()
            output.write(self.string.ljust(0x100, '\0').encode('utf-8'))
            output.write(b'\00' * 8)
            output.write(pack("<i", self.constant1))
            output.write(pack("<i", self.width))
            output.write(pack("<i", self.height))
            output.write(pack("<i", self.constant2))
            output.write(pack("<i", self.mipmap_count))
            output.write(pack("<i", self.face_count))
            output.write(pack("<i", self.type))
            output.write(b'\00' * 8)
            output.write(pack("<i", self.size))
            output.write(pack("<i", 0))
            output.write(pack("<i", self.size2))
            output.write(pack("<i", self.offset))
            output.write(pack("<i", 0))
            output.write(pack("<i", self.size3))
            output.write(pack("<i", 0))

            return output.getvalue()

        def save(self, path):
            with open(path, "wb") as file:
                file.write(self.compile_data())

    def __init__(self, data):
        compressed_data = h1a_compressed_data(data)
        self.data = compressed_data.decompress()
        stream = io.BytesIO(self.data)

        #get the child count, and load the child data
        self.count = int.from_bytes(stream.read(4), "little")
        stream.read(4)

        #load the imeta, and texture data
        for i in range(self.count):
            item = self.imeta()
            item.load_from_stream(stream)
            item.parse_block_data(io.BytesIO(self.data[item.offset : item.offset + item.size]))
            self.items.update({item.string : item})

    def recalculate_offsets(self):
        offset = 0x00290008
        for item in self.items.values():
            item.offset = offset
            offset += 58 + len(item.data.data)

    def save(self, path):
        output = io.BytesIO(self.data)
        self.recalculate_offsets()

        output.write(pack("<i", len(self.items)))
        output.write(pack("<i", 0))
        for item in self.items.values():
            output.write(item.compile_data())

        output.write(b'\0' * (0x00290008 - output.tell()))
        for item in self.items.values():
            output.write(item.data.compile_data_with_header())

        output.write(b'\0' * 0x0001ffff)

        with open(path, "wb") as file:
            file.write(output.getvalue())
