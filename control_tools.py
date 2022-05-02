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

def parent_constrain_controls():
    # Set up variables
    sels = cmds.ls(sl=True)
    constraint_target = sels[len(sels)-1]

    for i in range(len(sels)):
        if i >= len(sels)-1:
            break

        ctrl = sels[i]

        ctrl_grp = cmds.listRelatives(ctrl, parent=True)[0]

        # Create Constraints
        t_constraint = cmds.parentConstraint(constraint_target,
                                             ctrl_grp,
                                             maintainOffset=True,
                                             skipRotate=["x", "y", "z"],
                                             weight=1)[0]
        r_constraint = cmds.parentConstraint(constraint_target,
                                             ctrl_grp,
                                             maintainOffset=True,
                                             skipTranslate=["x", "y", "z"],
                                             weight=1)[0]

        # Create Attributes
        t_attr = "FollowTranslate"
        if not cmds.objExists(f"{ctrl}.{t_attr}"):
            cmds.addAttr(ctrl,
                         longName=t_attr,
                         attributeType="double",
                         min=0,
                         max=1,
                         defaultValue=1)
        t_attr = f"{ctrl}.{t_attr}"
        cmds.setAttr(t_attr, e=True, keyable=True)

        r_attr = "FollowRotate"
        if not cmds.objExists(f"{ctrl}.{r_attr}"):
            cmds.addAttr(ctrl,
                         longName=r_attr,
                         attributeType="double",
                         min=0,
                         max=1,
                         defaultValue=1)
        r_attr = f"{ctrl}.{r_attr}"
        cmds.setAttr(r_attr, e=True, keyable=True)

        # Connect Attributes
        cmds.connectAttr(t_attr,
                         f"{t_constraint}.w0",
                         force=True)
        cmds.connectAttr(r_attr,
                         f"{r_constraint}.w0",
                         force=True)

def parent_scale_constraints():
    sels = cmds.ls(sl=True)

    child = sels[0]
    parent = sels[1]
    cmds.parentConstraint(parent, child, maintainOffset=True, weight=1)
    cmds.scaleConstraint(parent, child, maintainOffset=True, weight=1)

def auto_constrain_joints_to_selected_controls():
    sels = cmds.ls(sl=True)

    for control in sels:
        if control.count("_") > 0:
            name_parts = control.rpartition("_")
            if name_parts[2] == "Ctrl":
                joint = name_parts[0] + "_Jnt"
                cmds.parentConstraint(control, joint, maintainOffset=True, weight=1)
                cmds.scaleConstraint(control, joint, maintainOffset=True, weight=1)

def mirror_controls():
    sels = cmds.ls(sl=True)

    # for each selected control...
    for control in sels:
        if control.count("_") > 0:
            name_parts = control.rpartition("_")
            if name_parts[2] == "Ctrl":
                # duplicate the control's group
                group = control + "_Grp"
                original_prefix = "L_"
                new_prefix = "R_"
                if "R_" in group:
                    original_prefix = "R_"
                    new_prefix = "L_"

                duplicate_grp = cmds.duplicate(group, name=group.replace(original_prefix, new_prefix), returnRootsOnly=True)[0]

                # rename duplicated control and
                # delete everything else that what duplicated (constraints, IK handles, etc)
                duplicate_children = cmds.listRelatives(duplicate_grp, children=True)
                for child in duplicate_children:
                    if child.count("_") > 0:
                        name_parts = child.rpartition("_")
                        if name_parts[2] == "Ctrl":
                            child = cmds.rename(duplicate_grp+"|"+child, child.replace(original_prefix, new_prefix))
                        else:
                            cmds.delete(duplicate_grp+"|"+child)

                # match transforms to joint
                joint = duplicate_grp.rpartition("_Ctrl_Grp")[0] + "_Jnt"
                cmds.matchTransform(duplicate_grp, joint)

                # inverse scale
                cmds.scale(-1, -1, -1, duplicate_grp)

                # freeze scale
                cmds.makeIdentity(duplicate_grp, apply=True, scale=True)
