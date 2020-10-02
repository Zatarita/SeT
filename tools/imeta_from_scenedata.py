from saber.file.ipak import Ipak
from common.data_parsing import StreamWriter


def imeta_from_scenedata(scenedata, inplace1_loc, inplace2_loc):
    inplace1 = inplace1_loc
    inplace2 = inplace2_loc

    if type(inplace1_loc) != Ipak:
        print("Loading inplace1..")
        print("\t" + inplace1_loc)
        inplace1 = Ipak(inplace1_loc)
    if type(inplace1_loc) != Ipak:
        print("Loading inplace2..")
        print("\t" + inplace2_loc)
        inplace2 = Ipak(inplace1_loc)

    print("Finding dependancies")
    output = StreamWriter()

    output.writeInt(len(scenedata.Textures) + 14)
    output.writeInt(0)

    unlisted_names = ['arifle_display_i1', 'expl_flame', 'font_main_00',
                      'menu_common_i17', 'menu_common_i7', 'menu_manager_i54',
                      'menu_manager_i5f', 'msg_box_i6', 'part_alias_akill',
                      'part_alias_normal', 'part_alias_transp', 'part_plasma',
                      'scorch_pak_parallax', 'xbox_rt_b', 'smoke_sm',
                      'part_rmp_flame_01']

    dependancies = scenedata.Textures + unlisted_names
    dependancies.sort()

    print("Writing dependancies")
    for texture in dependancies:
        dependant = inplace1.items.get(texture, None)
        dependant = inplace2.items.get(texture, dependant)
        if dependant:
            output.write(dependant.compile_data())

    print("Finalizing")
    output.write(b'\0' * (0x00290008 - output.tell()))
    return output.getvalue()
