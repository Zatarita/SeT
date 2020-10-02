from io import BytesIO
from struct import pack


class StreamParser(BytesIO):
    def __init__(self, data):
        BytesIO.__init__(self, data)

    # return an int of specified length from the byte stream
    def readInt(self, length):
        return int.from_bytes(self.read(length), "little")

    def readString(self, encoding="utf-8", null_terminated=True, length=-1):
        if not length:
            return
        if length > 0:
            null_terminated = False

        if null_terminated:
            string_builder = ""
            char_buffer = self.read(1).decode(encoding)

            while char_buffer != '\0':
                string_builder += char_buffer
                char_buffer += self.read(1).decode(encoding)

            return string_builder
        else:
            if length >= 0:
                return self.read(length).decode(encoding)

    # burn padding of set length
    def burn(self, length):
        self.read(length)


class StreamWriter(BytesIO):
    def __init__(self, endian="<"):
        BytesIO.__init__(self)
        self.endian = endian

    def writeInt(self, data):
        self.write(pack(self.endian + "I", data))

    def writeString(self, string, encoding="utf-8"):
        self.write(string.encode(encoding))
