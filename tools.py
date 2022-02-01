import maya.cmds as cmds


def change_color(name, color_index):
    shape = ''
    if cmds.attributeQuery('overrideColor', exists=True, node=name):
        shape = name
    else:
        shapes = cmds.listRelatives(name, shapes=True)
        if shapes is None:
            return
        shape = shapes[0]

    cmds.setAttr(f"{shape}.overrideEnabled", 1)
    cmds.setAttr(f"{shape}.overrideColor", color_index)


def sequential_rename_selection(name_pattern, start_num=1):

    # Get Selection #
    sels = cmds.ls(sl=True)

    # number of zeroes needed for zfill #
    z_count = name_pattern.count("#")

    # error out if no "#" symbols were found #
    if z_count == 0:
        print("name_pattern must include \"#\" symbols")
        return

    # generate "#" symbols for partition #
    z_place_holder = ""
    for z in range(z_count):
        z_place_holder += "#"

    # partition #
    par = name_pattern.partition(z_place_holder)

    # error out if "#" symbols are in multiple parts of the string
    if par[1] != z_place_holder:
        print("\"#\" symbols cannot be in multiple parts of the name_pattern")
        return

    # rename #
    for i in range(len(sels)):
        new_name = par[0]
        new_name += str(start_num + i).zfill(z_count)
        new_name += par[2]
        obj = cmds.rename(sels[i], new_name)
        print(f"{sels[i]} renamed to {obj}")