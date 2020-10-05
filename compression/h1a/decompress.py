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
    count = 0
    stream = StreamParser(data)
    offsets = []
    blocks = []

    # read the chunk count
    count = stream.readInt(4)

    # read offsets
    for i in range(count):
        offsets.append(stream.readInt(4))
    # temporary offset to calculate last - end
    offsets.append(len(data))
    # seek to first entry
    stream.seek(offsets[0])
    stream.burn(4)
    # read the blocks
    for i in range(count):
        blocks.append(stream.read(offsets[i+1] - offsets[i]))

    # using a file buffer to mitigate ram issues
    with open("tmp", "wb") as file:
        for i in range(len(blocks)):
            file.write(zlib.decompress(blocks[i]))
    # read the buffer back
    with open("tmp", "rb") as file:
        decompressed_data = file.read()

    # cleanup
    os.remove("tmp")
    return decompressed_data
