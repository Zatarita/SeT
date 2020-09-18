from directx.header import DDS_TEXTURE
from common.data_parsing import *
from struct import pack

def align(number, mask):
    if number == 0:
        return 0
    while mask % 2 == 0:
        number //= 2
        mask //= 2
    return number

def convert16To32(texture: DDS_TEXTURE):
    pixelStream = StreamParser(texture.pixelData)
    output = StreamWriter()
    while pixelStream.tell() < len(texture.pixelData):
        pixel = int.from_bytes(pixelStream.read(2), "little")
        a = align(pixel & texture.header.ddspf.ABitMask, texture.header.ddspf.ABitMask)
        r = align(pixel & texture.header.ddspf.RBitMask, texture.header.ddspf.RBitMask)
        g = align(pixel & texture.header.ddspf.GBitMask, texture.header.ddspf.GBitMask)
        b = align(pixel & texture.header.ddspf.BBitMask, texture.header.ddspf.BBitMask)
        r += 128
        g += 128
        b += 128

        output.write(a.to_bytes(1, "little"))
        output.write(r.to_bytes(1, "little"))
        output.write(g.to_bytes(1, "little"))
        output.write(b.to_bytes(1, "little"))

    return output.getvalue()
