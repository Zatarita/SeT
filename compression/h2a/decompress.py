import zlib, os
from common.data_parsing import StreamParser


def decompressor(data):
    stream = StreamParser(data)
    count = stream.readInt(8)
    print(count)

    offsets = [stream.readInt(8) for i in range(count)]
    offsets.append(len(data))

    with open("tmp", "wb") as file:
        for i in range(len(offsets) - 1):
            file.write(zlib.decompress(data[offsets[i] : offsets[i + 1]]))

    decompressed_data = open("tmp", "rb").read()

    os.remove("tmp")

    return decompressed_data