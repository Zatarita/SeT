from common.data_parsing import StreamParser, StreamWriter
import zlib
import os

"""
    compressor
        Function to compress a file
            data: data to be compressed
            return: compressed data
"""
def compressor(data):
    stream = StreamParser(data)
    chunks = []
    header = StreamWriter()

    # chunkify the data into chunks of 0x20000 bytes
    while (chunk := stream.read(0x20000)):
        chunks.append(chunk)

    # Open a file to use as a file buffer for the compression
    with open("tmp", "wb") as file:
        # prime the header with chunk count
        header.writeInt(len(chunks))
        # first offset
        offset = 0x40000

        for chunk in chunks:
            # write the offset to the header
            header.writeInt(offset)

            # compress the chunk
            compressed_chunk = zlib.compress(chunk,level=4)
            # update the offset to include the size of the compressed chunk
            offset += len(compressed_chunk)
            # write the compressed chunk
            file.write(compressed_chunk)

    # the header has a fixed size of 0x40000
    header.write(b'\0' * (0x40000 - header.tell()))
    # the first chunk has the max chunk size as the first four bytes
    header.writeInt(0x20000)

    # read back the file buffer
    with open("tmp", "rb") as file:
        compressed_data = file.read()

    # Remove the file buffer
    os.remove("tmp")

    # Combind the header to the compressed data, and return the entire block
    return header.getvalue() + compressed_data
