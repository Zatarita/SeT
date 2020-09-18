from directx.header import *


class Dxt5a(DDS_TEXTURE):
    def __init__(self):
        DDS_HEADER.__init__(self)
        self.header.ddspf.flags = self.header.ddspf.dwFlags.DDPF_FOURCC
        self.header.ddspf.fourCC = "ATI1"