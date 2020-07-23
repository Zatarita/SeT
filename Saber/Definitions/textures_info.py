from io import BytesIO
from struct import pack

class textures_info:
    items = []

    def __init__(self, data= None):
        if data: self.load(data)

    def load(self, data):
        stream = BytesIO(data)
        while stream.tell() < len(data):
            string_length = int.from_bytes(stream.read(4), "little")
            self.items.append(stream.read(string_length).decode("ANSI"))
            stream.seek(stream.tell() + 28)

    def add_entry(self, string):
        self.items.append(string)

    def add_entries(self, strings):
        for item in strings:
            self.items.append(item)

    def delete(self, string):
        del self.items[string]

    def compile_data(self):
        output = BytesIO()
        self.items.sort()
        for item in self.items:
            output.write(pack("<i", len(item)))
            output.write(item.encode("utf-8"))
            output.write(pack("<i", 0))
            output.write(pack("<i", 0))
            output.write(pack("<i", 0))
            output.write(pack("<i", 1))
            output.write(pack("<i", 1))
            output.write(pack("<i", 1))
            output.write(pack("<i", 0))
        return output.getvalue()

    def save(self, path):
        with open(path, "wb") as file:
            file.write(self.compile_data())
