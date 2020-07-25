import io
from struct import pack

class scene_data():
    size = 0

    SceneData = []
    CacheBlock = []
    Textures = []
    SoundData = []
    Templates = []
    VoiceSplines = []
    Scene = []
    Hkx = []
    TexturesDistanceFile = []
    CheckPointTexFile = []
    SceneRain = []
    SceneGrs = []
    SceneCDT = []
    SceneSM = []
    SceneVis = []

    def __init__(self, data = None):
        self.map = {
        "SceneData" : self.SceneData,
        "CacheBlock" : self.CacheBlock,
        "Textures" : self.Textures,
        "SoundData" : self.SoundData,
        "Templates" : self.Templates,
        "VoiceSplines" : self.VoiceSplines,
        "Scene" : self.Scene,
        "Hkx" : self.Hkx,
        "TexturesDistanceFile" : self.TexturesDistanceFile,
        "CheckPointTexFile" : self.CheckPointTexFile,
        "SceneRain" : self.SceneRain,
        "SceneGrs" : self.SceneGrs,
        "SceneCDT" : self.SceneCDT,
        "SceneSM" : self.SceneSM,
        "SceneVis" : self.SceneVis
        }
        if data: self.load(data)

    def compile_data(self):
        string = ""

        for label, object in self.map.items():
            label = list(set(object))
            if not object: continue
            string += label + "    =    [\n"
            for item in object:
                string += '\t"' + item + '"'
                if item != object[-1:][0]: string += "," #if not last item add coma
                string += "\n"
            string += "]\n"

        output = io.BytesIO()
        output.write(pack("<i", len(string)))
        output.write(string.encode("utf-8"))

        return output.getvalue()

    def save(self, path):
        with open(path, "wb") as file:
            file.write(self.compile_data())

    def load(self, data):
        stream = io.BytesIO(data)
        self.size = int.from_bytes(stream.read(4), "little")
        self.data = stream.read(len(data) - 4).decode("utf-8")

        for label, item in self.map.items():
            index = self.data.find(label + " ")
            if index > -1:
                substring = self.data[index+len(label) + 13:]
                item += substring[:substring.find('"\n]')].split('",\n\t"')
