from directx.header import *


class ARGB8888(DDS_TEXTURE):
    def __init__(self):
        DDS_TEXTURE.__init__(self)
        self.header.ddspf.flags = self.header.ddspf.dwFlags.DDPF_ALPHAPIXELS | self.header.ddspf.dwFlags.DDPF_RGB
        self.header.ddspf.RGBBitCount = 32
        self.header.ddspf.RBitMask = 0x000000ff
        self.header.ddspf.GBitMask = 0x0000ff00
        self.header.ddspf.BBitMask = 0x00ff0000
        self.header.ddspf.ABitMask = 0xff000000
