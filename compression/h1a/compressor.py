from common.data_parsing import StreamParser, StreamWriter
import zlib
import os


def compressor(data):
    stream = StreamParser(data)
    chunks = []
    header = StreamWriter()

    while chunk := stream.read(0x20000):
        chunks.append(chunk)

    with open("tmp", "wb") as file:
        header.writeInt(len(chunks))
        offset = 0x40000

        for chunk in chunks:
            header.writeInt(offset)

            compressed_chunk = zlib.compress(chunk,level=4)
            offset += len(compressed_chunk)
            file.write(compressed_chunk)

    header.write(b'\0' * (0x40000 - header.tell()))
    header.writeInt(0x20000)

    with open("tmp", "rb") as file:
        compressed_data = file.read()

    os.remove("tmp")

    return header.getvalue() + compressed_data
