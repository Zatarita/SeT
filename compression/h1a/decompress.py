import zlib
import os

from common.data_parsing import StreamParser

"""
    decompressor:
        Function to handle decomrpessing h1a files
            data: compressed data
            return: decompressed data (surprising)
"""

def decompressor(data):
    stream = StreamParser(data)
    # read the chunk count
    count = stream.readInt(4)

    # read offsets
    offsets = [(stream.readInt(4) + 4) for i in range(count)]
    # temporary offset to calculate last - end
    offsets.append(len(data))

    with open("tmp", "wb") as file:
        for i in range(len(offsets) - 1):
            chunk = zlib.decompress(data[offsets[i] : offsets[i + 1]])
            file.write(chunk)

    # read the buffer back
    with open("tmp", "rb") as file:
        decompressed_data = file.read()

    # cleanup
    os.remove("tmp")
    return decompressed_data
