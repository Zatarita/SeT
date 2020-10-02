from saber.file.ipak import Ipak
from os import listdir


ipak = Ipak("D:/SteamLibrary/steamapps/common/Halo The Master Chief Collection/halo1/prebuild/paks/inplace1.ipak")

ipak.save("inplace1.ipak_decompressed")

