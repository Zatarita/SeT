import io
from struct import pack


class imeta():
    items = {}

    class item():
        #empty item
        def __init__(self, stream = None):
            if not stream: return
            self.load(stream)

        #load item from stream
        def load(self, stream):
            self.string = stream.read(0x108).decode("ANSI").rstrip('\0')
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

    def __init__(self, data = None):
        if not data: return
        self.load(data)

    def load(self, data):
        self.items.clear()
        stream = io.BytesIO(data)
        count = int.from_bytes(stream.read(4), "little")
        stream.read(4)

        for i in range(count):
            item = self.item(stream)
            self.items.update({item.string : item})

    def save(self, path):
        with open(path, "wb") as file:
            file.write(pack("<i", len(self.items)))
            file.write(b'\0' * 4)
            for item in self.items:
                file.write(item.compile_data())
            file.write(b'\0' * (0x290008 - file.tell()))

    def names(self):
        return list(self.items.keys())

    def find(self, string):
        for i in range(len(self.items)):
            if list(self.items.keys())[i] == string:
                return i
        return -1

    def item_at_index(self, index):
        if index > len(self.items) or index == -1:
            return
        return list(self.items.values())[index]

    def delete(self, name):
        del self.items[name]
