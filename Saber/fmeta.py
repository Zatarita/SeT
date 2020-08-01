import io
from struct import pack

from Compression.Generation1.decompress import h1a_compressed_data

class fmeta():

    class item():
        string = ""
        type = 0
        decompressed_size = -1

        def __init__(self, stream = None):
            if not stream: return
            self.load_from_stream(stream)

        def load_from_stream(self, stream):
            self.string = stream.read(0x100).decode("utf-8").rstrip("\0")
            stream.read(4) #burn padding
            self.type = int.from_bytes(stream.read(4), "little")
            self.decompressed_size = int.from_bytes(stream.read(4), "little")
            stream.read(4) #burn padding

        def generate_from_file(self, string, type, size):

            self.string = string
            self.type = type
            self.size = size

    def __init__(self, data = None):
        self.items = []

        if type(data) == str:
            with open(data, "rb") as file:
                data = file.read()

        if not data: return
        self.load(data)

    def load(self, data):
        self.items.clear()
        stream = io.BytesIO(data)
        count = int.from_bytes(stream.read(4), "little")
        stream.read(4) #burn padding

        for i in range(count):
            self.items.append(self.item(stream))

    def compile_data(self):
        output = io.BytesIO()
        output.write(pack("<i", len(self.items)))
        output.write(b"\0" * 4)
        for item in self.items:
            output.write(item.string.ljust(0x100, "\0").encode("utf-8"))
            output.write(b'\0' * 4)
            output.write(pack("<i", item.type))
            if item.type == 0:
                output.write(b'\xff' * 8)
            else:
                output.write(pack("<i", item.decompressed_size))
                output.write(b'\00' * 4)

        output.write(b'\0' * (0x4408 - output.tell()))

        return output.getvalue()

    def add_entry(self, file, size = -1):
        if len(self.items) == 40:
            print("Exceeds maximum file size. Ignoring entry.")
            return
        new_item = self.item()
        if file in self.items:
            return
        if size == 0:
            new_item.generate_from_file(file, 0 ,size)
        else:
            new_item.generate_from_file(file, 1, size)

        self.items.append(new_item)
        self.items.sort()

    def delete(self, string):
        for item in self.items:
            if item.string == string:
                self.items.remove(item)

    def get_decompressed_size(path):
        with open(path, "rb") as file:
            content = file.read()
        map_data = h1a_compressed_data(content)
        return len(map_data.decompress())

    def save(self, path):
        with open(path, "wb") as file:
            file.write(self.compile_data())
