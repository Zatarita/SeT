from enum import IntFlag, Enum, auto
from common.data_parsing import StreamWriter, StreamParser


# dwFlag values for ddsHeader.flags
class dwFlags(IntFlag):
    DDSD_CAPS = 0x1
    DDSD_HEIGHT = 0x2
    DDSD_WIDTH = 0x4
    DDSD_PITCH = 0x8
    DDSD_PIXELFORMAT = 0x1000
    DDSD_MIPMAPCOUNT = 0x20000
    DDSD_LINEARSIZE = 0x80000
    DDSD_DEPTH = 0x800000

# dwCaps values for ddsHeader.caps
class dwCaps(IntFlag):
    DDSCAPS_COMPLEX = 0x8
    DDSCAPS_TEXTURE = 0x1000
    DDSCAPS_MIPMAP = 0x400000

# dwCaps2 values for ddsHeader.caps2
class dwCaps2(IntFlag):
    DDSCAPS2_CUBEMAP = 0x200
    DDSCAPS2_CUBEMAP_POSITIVEX = 0x400
    DDSCAPS2_CUBEMAP_NEGATIVEX = 0x800
    DDSCAPS2_CUBEMAP_POSITIVEY = 0x1000
    DDSCAPS2_CUBEMAP_NEGATIVEY = 0x2000
    DDSCAPS2_CUBEMAP_POSITIVEZ = 0x4000
    DDSCAPS2_CUBEMAP_NEGATIVEZ = 0x8000
    DDS_CUBEMAP_ALLFACES = 0xfe00
    DDSCAPS2_VOLUME = 0x200000

# values for DDS_HEADER_DXT10.dxgiFormat
class DXGI_FORMAT(Enum):
    DXGI_FORMAT_UNKNOWN = auto()
    DXGI_FORMAT_R32G32B32A32_TYPELESS = auto()
    DXGI_FORMAT_R32G32B32A32_FLOAT = auto()
    DXGI_FORMAT_R32G32B32A32_UINT = auto()
    DXGI_FORMAT_R32G32B32A32_SINT = auto()
    DXGI_FORMAT_R32G32B32_TYPELESS = auto()
    DXGI_FORMAT_R32G32B32_FLOAT = auto()
    DXGI_FORMAT_R32G32B32_UINT = auto()
    DXGI_FORMAT_R32G32B32_SINT = auto()
    DXGI_FORMAT_R16G16B16A16_TYPELESS = auto()
    DXGI_FORMAT_R16G16B16A16_FLOAT = auto()
    DXGI_FORMAT_R16G16B16A16_UNORM = auto()
    DXGI_FORMAT_R16G16B16A16_UINT = auto()
    DXGI_FORMAT_R16G16B16A16_SNORM = auto()
    DXGI_FORMAT_R16G16B16A16_SINT = auto()
    DXGI_FORMAT_R32G32_TYPELESS = auto()
    DXGI_FORMAT_R32G32_FLOAT = auto()
    DXGI_FORMAT_R32G32_UINT = auto()
    DXGI_FORMAT_R32G32_SINT = auto()
    DXGI_FORMAT_R32G8X24_TYPELESS = auto()
    DXGI_FORMAT_D32_FLOAT_S8X24_UINT = auto()
    DXGI_FORMAT_R32_FLOAT_X8X24_TYPELESS = auto()
    DXGI_FORMAT_X32_TYPELESS_G8X24_UINT = auto()
    DXGI_FORMAT_R10G10B10A2_TYPELESS = auto()
    DXGI_FORMAT_R10G10B10A2_UNORM = auto()
    DXGI_FORMAT_R10G10B10A2_UINT = auto()
    DXGI_FORMAT_R11G11B10_FLOAT = auto()
    DXGI_FORMAT_R8G8B8A8_TYPELESS = auto()
    DXGI_FORMAT_R8G8B8A8_UNORM = auto()
    DXGI_FORMAT_R8G8B8A8_UNORM_SRGB = auto()
    DXGI_FORMAT_R8G8B8A8_UINT = auto()
    DXGI_FORMAT_R8G8B8A8_SNORM = auto()
    DXGI_FORMAT_R8G8B8A8_SINT = auto()
    DXGI_FORMAT_R16G16_TYPELESS = auto()
    DXGI_FORMAT_R16G16_FLOAT = auto()
    DXGI_FORMAT_R16G16_UNORM = auto()
    DXGI_FORMAT_R16G16_UINT = auto()
    DXGI_FORMAT_R16G16_SNORM = auto()
    DXGI_FORMAT_R16G16_SINT = auto()
    DXGI_FORMAT_R32_TYPELESS = auto()
    DXGI_FORMAT_D32_FLOAT = auto()
    DXGI_FORMAT_R32_FLOAT = auto()
    DXGI_FORMAT_R32_UINT = auto()
    DXGI_FORMAT_R32_SINT = auto()
    DXGI_FORMAT_R24G8_TYPELESS = auto()
    DXGI_FORMAT_D24_UNORM_S8_UINT = auto()
    DXGI_FORMAT_R24_UNORM_X8_TYPELESS = auto()
    DXGI_FORMAT_X24_TYPELESS_G8_UINT = auto()
    DXGI_FORMAT_R8G8_TYPELESS = auto()
    DXGI_FORMAT_R8G8_UNORM = auto()
    DXGI_FORMAT_R8G8_UINT = auto()
    DXGI_FORMAT_R8G8_SNORM = auto()
    DXGI_FORMAT_R8G8_SINT = auto()
    DXGI_FORMAT_R16_TYPELESS = auto()
    DXGI_FORMAT_R16_FLOAT = auto()
    DXGI_FORMAT_D16_UNORM = auto()
    DXGI_FORMAT_R16_UNORM = auto()
    DXGI_FORMAT_R16_UINT = auto()
    DXGI_FORMAT_R16_SNORM = auto()
    DXGI_FORMAT_R16_SINT = auto()
    DXGI_FORMAT_R8_TYPELESS = auto()
    DXGI_FORMAT_R8_UNORM = auto()
    DXGI_FORMAT_R8_UINT = auto()
    DXGI_FORMAT_R8_SNORM = auto()
    DXGI_FORMAT_R8_SINT = auto()
    DXGI_FORMAT_A8_UNORM = auto()
    DXGI_FORMAT_R1_UNORM = auto()
    DXGI_FORMAT_R9G9B9E5_SHAREDEXP = auto()
    DXGI_FORMAT_R8G8_B8G8_UNORM = auto()
    DXGI_FORMAT_G8R8_G8B8_UNORM = auto()
    DXGI_FORMAT_BC1_TYPELESS = auto()
    DXGI_FORMAT_BC1_UNORM = auto()
    DXGI_FORMAT_BC1_UNORM_SRGB = auto()
    DXGI_FORMAT_BC2_TYPELESS = auto()
    DXGI_FORMAT_BC2_UNORM = auto()
    DXGI_FORMAT_BC2_UNORM_SRGB = auto()
    DXGI_FORMAT_BC3_TYPELESS = auto()
    DXGI_FORMAT_BC3_UNORM = auto()
    DXGI_FORMAT_BC3_UNORM_SRGB = auto()
    DXGI_FORMAT_BC4_TYPELESS = auto()
    DXGI_FORMAT_BC4_UNORM = auto()
    DXGI_FORMAT_BC4_SNORM = auto()
    DXGI_FORMAT_BC5_TYPELESS = auto()
    DXGI_FORMAT_BC5_UNORM = auto()
    DXGI_FORMAT_BC5_SNORM = auto()
    DXGI_FORMAT_B5G6R5_UNORM = auto()
    DXGI_FORMAT_B5G5R5A1_UNORM = auto()
    DXGI_FORMAT_B8G8R8A8_UNORM = auto()
    DXGI_FORMAT_B8G8R8X8_UNORM = auto()
    DXGI_FORMAT_R10G10B10_XR_BIAS_A2_UNORM = auto()
    DXGI_FORMAT_B8G8R8A8_TYPELESS = auto()
    DXGI_FORMAT_B8G8R8A8_UNORM_SRGB = auto()
    DXGI_FORMAT_B8G8R8X8_TYPELESS = auto()
    DXGI_FORMAT_B8G8R8X8_UNORM_SRGB = auto()
    DXGI_FORMAT_BC6H_TYPELESS = auto()
    DXGI_FORMAT_BC6H_UF16 = auto()
    DXGI_FORMAT_BC6H_SF16 = auto()
    DXGI_FORMAT_BC7_TYPELESS = auto()
    DXGI_FORMAT_BC7_UNORM = auto()
    DXGI_FORMAT_BC7_UNORM_SRGB = auto()
    DXGI_FORMAT_AYUV = auto()
    DXGI_FORMAT_Y410 = auto()
    DXGI_FORMAT_Y416 = auto()
    DXGI_FORMAT_NV12 = auto()
    DXGI_FORMAT_P010 = auto()
    DXGI_FORMAT_P016 = auto()
    DXGI_FORMAT_420_OPAQUE = auto()
    DXGI_FORMAT_YUY2 = auto()
    DXGI_FORMAT_Y210 = auto()
    DXGI_FORMAT_Y216 = auto()
    DXGI_FORMAT_NV11 = auto()
    DXGI_FORMAT_AI44 = auto()
    DXGI_FORMAT_IA44 = auto()
    DXGI_FORMAT_P8 = auto()
    DXGI_FORMAT_A8P8 = auto()
    DXGI_FORMAT_B4G4R4A4_UNORM = auto()
    DXGI_FORMAT_P208 = auto()
    DXGI_FORMAT_V208 = auto()
    DXGI_FORMAT_V408 = auto()
    DXGI_FORMAT_SAMPLER_FEEDBACK_MIN_MIP_OPAQUE = auto()
    DXGI_FORMAT_SAMPLER_FEEDBACK_MIP_REGION_USED_OPAQUE = auto()
    DXGI_FORMAT_FORCE_UINT = auto()

# values for DDS_HEADER_DXT10.resourceDimension
class D3D10_RESOURCE_DIMENSION (Enum):
    D3D10_RESOURCE_DIMENSION_UNKNOWN = auto()
    D3D10_RESOURCE_DIMENSION_BUFFER = auto()
    D3D10_RESOURCE_DIMENSION_TEXTURE1D = auto()
    D3D10_RESOURCE_DIMENSION_TEXTURE2D = auto()
    D3D10_RESOURCE_DIMENSION_TEXTURE3D = auto()

# values for DDS_HEADER_DXT_10.miscFlag
class D3D10_RESOURCE_MISC_FLAG (Enum):
    D3D10_RESOURCE_MISC_GENERATE_MIPS = auto()
    D3D10_RESOURCE_MISC_SHARED = auto()
    D3D10_RESOURCE_MISC_TEXTURECUBE = auto()
    D3D10_RESOURCE_MISC_SHARED_KEYEDMUTEX = auto()
    D3D10_RESOURCE_MISC_GDI_COMPATIBLE = auto()

# values for DDS_HEADER_DXT_10.miscFlag
class D3D10_RESOURCE_MISC_FLAG2 (Enum):
    DDS_ALPHA_MODE_UNKNOWN = auto()
    DDS_ALPHA_MODE_STRAIGHT = auto()
    DDS_ALPHA_MODE_PREMULTIPLIED = auto()
    DDS_ALPHA_MODE_OPAQUE = auto()
    DDS_ALPHA_MODE_CUSTOM = auto()


# struct definition for dx10 header
class DDS_HEADER_DXT10:
    def __init__(self):
        self.dxgiFormat = 0
        self.resourceDimension = 0
        self.miscFlag = 0
        self.arraySize = 0
        self.miscFlags2 = 0

class DDS_PIXELFORMAT:
    # dwFlag values for ddsPixelFormat.flags
    class dwFlags(IntFlag):
        DDPF_ALPHAPIXELS = 0x1
        DDPF_ALPHA = 0x2
        DDPF_FOURCC = 0x4
        DDPF_RGB = 0x40
        DDPF_YUV = 0x200
        DDPF_LUMINANCE = 0x20000

    def __init__(self):
        self.size = 0x20
        self.flags = 0
        self.fourCC = ""
        self.RGBBitCount = 0
        self.RBitMask = 0
        self.GBitMask = 0
        self.BBitMask = 0
        self.ABitMask = 0

    def compile(self, stream: StreamWriter):
        stream.writeInt(self.size)
        stream.writeInt(self.flags)
        if self.fourCC:
            stream.writeString(self.fourCC)
        else:
            stream.writeInt(0)
        stream.writeInt(self.RGBBitCount)
        stream.writeInt(self.RBitMask)
        stream.writeInt(self.GBitMask)
        stream.writeInt(self.BBitMask)
        stream.writeInt(self.ABitMask)

    def load(self, stream: StreamParser):
        self.size = stream.readInt(4)
        self.flags = stream.readInt(4)
        self.fourCC = stream.readString(length=4)
        self.RGBBitCount = stream.readInt(4)
        self.RBitMask = stream.readInt(4)
        self.GBitMask = stream.readInt(4)
        self.BBitMask = stream.readInt(4)
        self.ABitMask = stream.readInt(4)



class DDS_HEADER:
    def __init__(self):
        self.magic = "DDS "
        self.size = 0x7c
        self.flags = dwFlags.DDSD_CAPS | dwFlags.DDSD_HEIGHT | dwFlags.DDSD_WIDTH | dwFlags.DDSD_PIXELFORMAT
        self.height = 0
        self.width = 0
        self.pitchOrLinearSize = 0
        self.depth = 0
        self.mipmap_count = 0
        self.reserved = [0] * 11
        self.ddspf = DDS_PIXELFORMAT()
        self.caps = 0
        self.caps2 = 0
        self.caps3 = 0 # unused
        self.caps4 = 0 # unused
        self.reserved2 = 0 # unused
        # self.headerDXT10 = DDS_HEADER_DXT10

    def compile(self):
        stream = StreamWriter()
        stream.writeString(self.magic)
        stream.writeInt(self.size)
        stream.writeInt(self.flags)
        stream.writeInt(self.height)
        stream.writeInt(self.width)
        stream.writeInt(self.pitchOrLinearSize)
        stream.writeInt(self.depth)
        stream.writeInt(self.mipmap_count)
        for item in self.reserved:
            stream.writeInt(0)
        self.ddspf.compile(stream)
        stream.writeInt(self.caps)
        stream.writeInt(self.caps2)
        stream.writeInt(self.caps3)
        stream.writeInt(self.caps4)
        stream.writeInt(self.reserved2)
        return stream.getvalue()

    def setDimensions(self, height: int, width: int):
        self.height = height
        self.width = width

    def load(self, path):
        if type(path) != StreamParser:
            stream = StreamParser(open(path, "rb").read())
        else:
            stream = path
        self.magic = stream.readString(length=4)
        self.size = stream.readInt(4)
        self.flags = stream.readInt(4)
        self.height = stream.readInt(4)
        self.width = stream.readInt(4)
        self.pitchOrLinearSize = stream.readInt(4)
        self.depth = stream.readInt(4)
        self.mipmap_count = stream.readInt(4)
        for item in self.reserved:
            stream.readInt(4)
        self.ddspf.load(stream)
        self.caps = stream.readInt(4)
        self.caps2 = stream.readInt(4)
        self.caps3 = stream.readInt(4)
        self.caps4 = stream.readInt(4)
        self.reserved2 = stream.readInt(4)

class DDS_TEXTURE:
    def __init__(self):
        self.header = DDS_HEADER()
        self.pixelData = None

    def load(self, path):
        stream = StreamParser(open(path, "rb").read())
        self.header.load(stream) # if stream passed instead of path, stream will be used
        self.pixelData = stream.read() # read pixel data

    def getFaceCount(self):
        if self.header.caps2 & dwCaps2.DDS_CUBEMAP_ALLFACES:
            return 6
        else:
            return 1

    def typeToHaloEnum(self):
        fourCC = {
            "DXT1": 13,
            "DXT3": 15,
            "DXT5": 17,
            "ATI1": 37,
            "ATI2": 36
        }
        # attempt to get the type from above switch
        fcc = fourCC.get(self.header.ddspf.fourCC, None)
        if fcc:
            # if it returns something, we've identified by the fourCC the type
            return fcc
        # if no type found by fourCC, it is either ai88, argb, or xrgb
        if self.header.ddspf.GBitMask == 0x0000ff00:
            # if there is a green channel mask
            if self.header.flags & DDS_PIXELFORMAT.dwFlags.DDPF_ALPHAPIXELS:
                return 0
            else:
                return 22
        else:
            return 10