from saber.file.ipak import Ipak
from os import listdir
import cProfile


ipak = Ipak("D:/SteamLibrary/steamapps/common/Halo The Master Chief Collection/halo1/prebuild/paks/inplace1.ipak")

cProfile.runctx("ipak.save('inplace1.ipak_decompressed')", globals(), locals())

