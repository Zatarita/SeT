from directx.header import *


class AI88(DDS_TEXTURE):
    def __init__(self):
        DDS_HEADER.__init__(self)
        self.header.ddspf.flags = self.header.ddspf.dwFlags.DDPF_ALPHAPIXELS | self.header.ddspf.dwFlags.DDPF_LUMINANCE
        self.header.ddspf.RGBBitCount = 16
        self.header.ddspf.RBitMask = 0x00ff0000
        self.header.ddspf.ABitMask = 0xff000000
