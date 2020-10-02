from directx.header import DDS_TEXTURE
from common.data_parsing import *
from struct import Struct

def get_shift_and_mask(mask):
    shift = 0
    while not (mask >> shift) & 1:
        shift += 1
    return shift, mask >> shift

def convert16To32(texture: DDS_TEXTURE):
    pixelStream = StreamParser(texture.pixelData)
    output = StreamWriter()

    # precalculate these since they never change

    a_shift, a_mask = get_shift_and_mask(texture.header.ddspf.ABitMask) if texture.header.ddspf.ABitMask \
                      else 0, 0
    r_shift, r_mask = get_shift_and_mask(texture.header.ddspf.RBitMask)
    g_shift, g_mask = get_shift_and_mask(texture.header.ddspf.GBitMask)
    b_shift, b_mask = get_shift_and_mask(texture.header.ddspf.BBitMask)

    # we are creating an anonymous Struct instance and grabbing a direct reference to its pack method
    pixel32_packer = Struct("<BBBB").pack

    while pixelStream.tell() < len(texture.pixelData):
        pixel = int.from_bytes(pixelStream.read(2), "little")
        # one pack and one write instead of 4
        alpha = ((((pixel >> a_shift) & a_mask) * 255) // a_mask) if a_mask else 255
        output.write(pixel32_packer(
            (((pixel >> r_shift) & r_mask) * 255) // r_mask,
            (((pixel >> g_shift) & g_mask) * 255) // g_mask,
            (((pixel >> b_shift) & b_mask) * 255) // b_mask,
            alpha))


    return output.getvalue()