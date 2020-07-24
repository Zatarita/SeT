import io
from struct import pack

from Compression.Generation1.decompress import h1a_compressed_data

class fmeta():
    items = []

    class item():
        string = ""
        type = -1
        decompressed_size = -1

        def __init__(self, stream = None):
            if stream = None: return
            self.load_from_stream(stream)

        def load_from_stream(self, stream):
            self.string = stream.read(0x100).decode("utf-8").rstrip("\0")
            stream.read(8) #burn padding
            self.type = int.from_bytes(stream.read(4), "little")
            self.decompressed_size = int.from_bytes(stream.read(4), "little")

        def generate_from_file(self, string, type, size):
            # TO-DO: the string is local to the halo directory

            self.string = "/Local/Halo/Directory/" + string
            self.type = type
            self.size = size

    def __init__(self, data = None):
        if data = None: return
        self.load(data)

    def load(self, data):
        stream = io.BytesIO(data)
        count = int.from_bytes(stream.read(4), "little")
        stream.read(4) #burn padding

        for i in range(count):
            items.append(self.item(stream))

    def compile_data(self):
        output = io.BytesIO()
        output.write(pack("<i", len(self.items)))
        output.write(b"\0" * 4)
        for item in self.items:
            output.write(item.string.ljust(0x100, "\0").encode("utf-8"))
            output.write('\0' * 8)
            output.write(pack("<i", item.type))
            output.write(pack("<i", item.decompressed_size))

        #TODO Update the 18kb with actual file size
        #output.write('\0' * 18kb - output.tell())

        return output.getvalue()

    def add_entry(self, file, size):
        new_item = self.item()
        if size == -1:
            new_item.generate_from_file(file, -1 ,size)
        else:
            new_item.generate_from_file(file, 1, size)

        self.items.append(new_item)

    def get_decompressed_size(path):
        with open(path, "rb") as file:
            content = file.read()
        map_data = h1a_compressed_data(content)
        return len(map_data.decompress())

    def save(self, path):
        with open(path, "wb") as file:
            file.write(self.compile_data())
