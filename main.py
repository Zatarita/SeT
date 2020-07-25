from Saber.s3dpak import s3dpak
from Saber.ipak import ipak
from Saber.imeta import imeta
from Saber.fmeta import fmeta
from tools.imeta_from_scenedata import imeta_from_scenedata
from Saber.Definitions.scene_data import scene_data
from Saber.Definitions.tpl import template
from Saber.Definitions.textures_info import textures_info

with open("C:/Users/Andy/Desktop/Halo - Research/Halo 1 Aniversary/Paks/a10/compressed/a10.s3dpak", "rb") as file:
    contents = file.read()
test = s3dpak(contents)
output = imeta_from_scenedata(scene_data(test.items["SceneData"].data),
                                         "C:/Users/Andy/Desktop/Halo - Research/Halo 1 Aniversary/Paks/initial/compressed/inplace1.ipak",
                                         "C:/Users/Andy/Desktop/Halo - Research/Halo 1 Aniversary/Paks/initial/compressed/inplace2.ipak" ,)
example = imeta(output)
exit()
