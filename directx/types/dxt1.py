from directx.header import *


class Dxt1(DDS_TEXTURE):
    def __init__(self):
        DDS_HEADER.__init__(self)
        self.header.ddspf.flags = self.header.ddspf.dwFlags.DDPF_FOURCC
        self.header.ddspf.fourCC = "DXT1"