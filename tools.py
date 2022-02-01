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


def create_controls(color_index=0, radius=1):
    # Create controls from multiple selections.
    sels = cmds.ls(sl=True)
    if len(sels) > 0:
        for sel in sels:
            control = create_single_control(name=sel, color_index=color_index, radius=radius)
            cmds.matchTransform(control[0], sel)
    else:
        create_single_control(color_index=color_index, radius=radius)


def create_controls_hierarchy(color_index=0, radius=1):
    # create controls based on a hierarchy. Single selection.
    sels = cmds.ls(sl=True)
    if not len(sels) == 1:
        cmds.error("Please select root object only.")
    parent = sels[0]
    create_child_control(color_index=color_index, name=parent, radius=radius)


def create_child_control(color_index=0, name="", radius=1):
    # a recursive function used by create_controls_hierarchy
    parent_control = create_single_control(name, color_index=color_index, radius=radius)
    cmds.matchTransform(parent_control[0], name)

    children = cmds.listRelatives(name, children=True, type="transform")
    if children == None:
        return parent_control

    print(children)

    for child in children:
        child_control = create_child_control(color_index=color_index, name=child, radius=radius)
        cmds.parent(child_control[0], parent_control[1])
    return parent_control


def create_single_control(name="Control", color_index=0, radius=1):
    # create a single control.
    # returns string array with the parent group and the control
    control_name = ""
    if name.count("_") > 0:
        name_parts = name.rpartition("_")
        control_name = name_parts[0] + "_Ctrl"
    else:
        control_name = name + "_Ctrl"

    group_name = control_name + "_Grp"

    control = cmds.circle(name=control_name, normal=(1, 0, 0), radius=radius)[0]
    # cmds.xform(control, rotation=(90, 0, 0))
    # cmds.makeIdentity(control, apply=True)

    change_color(control, color_index)

    group = cmds.group(control, name=group_name)
    return [group, control]


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