from Compression.Generation1.decompress import h1a_compressed_data

import io
from struct import pack

class s3dpak():


    type_definitions = {
    "Scene Data" : 0,
    "Data" : 1,
    "Single Player Lines" : 2,
    "Shader" : 3,
    "Textures Info" : 5,
    "Sound Data" : 8,
    "Memory" : 10,
    "Skull Data" : 11,
    "Template" : 12,
    "String List" : 14,
    "Game Logic" : 16,
    "Breakable glass" : 17,
    "Effects" : 18,
    "(.grs)" : 22,
    "Rain" : 25,
    "(.cdt)" : 26,
    "(.sm)" : 27,
    "(.vis)" : 29,
    }

    class item():
        #empty item
        def __init__(self):
            self.offset = 0
            self.size = 0
            self.string_length = 0
            self.string = ""
            self.type = 0

            self.data = None

        #load item from stream
        def load_from_stream(self, stream):
            self.offset = int.from_bytes(stream.read(4), "little")
            self.size = int.from_bytes(stream.read(4), "little")
            self.string_length = int.from_bytes(stream.read(4), "little")
            self.string = stream.read(self.string_length).decode("utf-8")
            self.type = int.from_bytes(stream.read(4), "little")

            pos = stream.tell() + 8
            stream.seek(self.offset)
            self.data = stream.read(self.size)
            stream.seek(pos)

            self.string = "SceneData" if self.string == "" else self.string

        #load item from file
        def load_from_file(self, path, type):
            with open(path, "rb") as file:
                self.data = file.read()

            self.offset = 0
            self.size = len(self.data)
            self.string = path.split("/")[len(path.split("/")) - 1]
            self.string_length = len(self.string)
            self.type = type

        #generate glossary entries
        def get_header(self):
            output = io.BytesIO()
            output.write(pack("<i", self.offset))
            output.write(pack("<i", self.size))
            if self.string == "SceneData":
                output.write(pack("<i", 0))
            else:
                output.write(pack("<i", self.string_length))
                output.write(self.string.encode("utf-8"))
            output.write(pack("<i", self.type))
            output.write(b"\x00" * 8)
            return output

        def save(self, path):
            with open(path, "wb") as file:
                file.write(self.data)

    #s3dpak object
    def __init__(self, data = None, percent_hook = None, status_hook = None):
        self.count = 0
        self.items = {}

        if type(data) == str:
            with open(data, "rb") as file:
                data = file.read()

        if data == None: return
        self.load(data, percent_hook, status_hook)

    def load(self, data, percent_hook = None, status_hook = None):
        self.data = h1a_compressed_data(data, percent_hook, status_hook).decompress()
        stream = io.BytesIO(self.data)

        #get the child count, and load the child data
        self.count = int.from_bytes(stream.read(4), "little")
        for i in range(self.count):
            item = self.item()
            item.load_from_stream(stream)
            self.items.update({item.string : item})

    #import a file into the s3dpak
    def import_file(self, path, data_type):
        item = self.item()
        if type(data_type) != int: data_type = self.type_definitions.get(data_type, -1)
        if not data_type in list(self.type_definitions.values()):
            print("Unknown type")
            return
        item.load_from_file(path, data_type)
        self.items.update({item.string : item})
        self.recalculate_offsets()

    #recalculate offsets for after a file change
    def recalculate_offsets(self):
        offset = 4
        #first pass to find out glossary size
        for item in self.items.values():
            offset += 24 + item.string_length

        #second pass to actually set the data
        for item in self.items.values():
            item.offset = offset
            offset += len(item.data)

    #save the s3dpak. if compressed is true, it will auto compress
    def save(self, path, compressed = True):
        out = io.BytesIO()
        #write the glossary
        out.write(pack("<i", len(self.items)))
        for item in self.items.values():
            out.write(item.get_header().getvalue())

        #write the data
        for item in self.items.values():
            out.write(item.data)

        with open(path, "wb") as file:
            file.write(out.getvalue())
        return

        #if compression requested, compress (broken)
        """if compressed:
            compressed_data = h1a_decompressed_data(out.getvalue()).compress()
            compressed_data.save(path)
        else:
            with open(path, "wb") as file:
                file.write(out.getvalue())"""

    def export_all(self, path):
        for item in self.items.values():
            item.save(path + "/" + item.string)

    def delete(self, item):
        del self.items[item]
        self.recalculate_offsets()

    def item_at_index(self, index):
        if index > len(self.items) or index == -1:
            return
        return list(self.items.values())[index]

    def find(self, item):
        for i in range(len(self.items)):
            if list(self.items.values())[i].string == item:
                return i
        return -1

    def names(self):
        return list(self.items.keys())

    def item_count(self):
        return len(self.items)
