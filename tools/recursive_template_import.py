from saber.file import *
from saber.definitions.scene_data import SceneData
from common.data_parsing import StreamParser
import os


def recursiveTemplateImport(target: SaberPak, imeta : Imeta, path):
    # load the SceneData
    scene_data = None
    if "SceneData" not in target.children:
        print("s3dpak not compatible. May be corrupted, SceneData not present.\n"
              "Execution can continue, but SceneData wont be updated")
    else:
        scene_data = SceneData()
        scene_data.load(target.children["SceneData"].data)

    files = os.listdir(path)
    for file in files:
        stream = StreamParser(open(path + "/" + file, "rb").read())
        name = file.split(".")[0].split("/")[-1]

        if ".imeta_child" in file:
            new_child = imeta.Child()
            new_child.loadFromStream(stream)
            imeta.importChild(file.split(".")[0], new_child)
            if scene_data:
                if name not in scene_data.Textures:
                    scene_data.Textures.append(name)
        else:
            target.addEntry(path + "/" + file, "Template")
            if scene_data:
                if name not in scene_data.Templates:
                    scene_data.Templates.append(name)

    if scene_data:
        target.children["SceneData"].data = scene_data.compile_data()

    return (target, imeta)