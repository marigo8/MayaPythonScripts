import maya.cmds as cmds
import tools

import importlib
importlib.reload(tools)

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

    tools.change_color(control, color_index)

    group = cmds.group(control, name=group_name)
    return [group, control]

def change_control_radius(radius=1):
    sels = cmds.ls(sl=True)
    for sel in sels:
        cmds.circle(sel, edit=True, radius=radius)