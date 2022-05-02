import maya.cmds as cmds
import importlib


class control_tools_ui:
    def __init__(self):
        self.m_window = 'controlToolsUIWin'
        self.override_color = 0
        self.colorSlider = ''
        self.controlRadiusField = ''

    def create(self):
        self.delete()

        self.m_window = cmds.window(self.m_window, title="Control Tools", resizeToFitChildren=True)
        column = cmds.columnLayout(parent=self.m_window)

        # change color
        self.colorSlider = cmds.colorIndexSliderGrp(parent=column,
                                                    label="OverrideColor",
                                                    minValue=1,
                                                    maxValue=32)
        cmds.button(parent=column, label="Apply Color", command=lambda *x: self.override_color_apply_cmd())
        cmds.button(parent=column, label="Apply Color To Hierarchy",
                    command=lambda *x: self.override_color_apply_hierarchy_cmd())

        # controls
        self.controlRadiusField = cmds.floatFieldGrp(parent=column, label="Control Radius", value1=1, changeCommand=lambda *x: self.change_control_radius_cmd())
        # cmds.button(parent=column, label="Change Control Radius", command=lambda *x: self.change_control_radius_cmd())

        cmds.button(parent=column, label="Create Controls", command=lambda *x: self.create_controls_cmd())
        cmds.button(parent=column, label="Create Controls From Hierarchy",
                    command=lambda *x: self.create_controls_hierarchy_cmd())
        cmds.button(parent=column, label="Parent Constrain Controls", command=lambda *x: self.parent_constrain_controls_cmd())
        cmds.button(parent=column, label="Parent Scale Constraints", command=lambda *x: self.parent_scale_constraints_cmd())
        cmds.button(parent=column, label="Auto Constrain Joints to Selected Controls", command=lambda *x: self.auto_constrain_joints_to_selected_controls_cmd())
        cmds.button(parent=column, label="Mirror Controls", command=lambda *x: self.mirror_controls_cmd())

        self.show()

    def delete(self):
        if cmds.window(self.m_window, exists=True):
            cmds.deleteUI(self.m_window)

    def show(self):
        if cmds.window(self.m_window, exists=True):
            cmds.showWindow(self.m_window)

    def get_color(self):
        return cmds.colorIndexSliderGrp(self.colorSlider, q=True, value=True) - 1

    def override_color_apply_cmd(self):
        import tools
        importlib.reload(tools)
        sels = cmds.ls(sl=True)
        for sel in sels:
            tools.change_color(sel, self.get_color())
        return

    def override_color_apply_hierarchy_cmd(self):
        import tools
        importlib.reload(tools)
        sels = cmds.ls(sl=True)
        for sel in sels:
            tools.change_color(sel, self.get_color())
            children = cmds.listRelatives(sel, allDescendents=True)
            for child in children:
                tools.change_color(child, self.get_color())
        return

    def get_control_radius(self):
        return cmds.floatFieldGrp(self.controlRadiusField, q=True, value1=True)

    def create_controls_cmd(self):
        import control_tools
        importlib.reload(control_tools)

        control_tools.create_controls(self.get_color(), radius=self.get_control_radius())

    def create_controls_hierarchy_cmd(self):
        import control_tools
        importlib.reload(control_tools)

        control_tools.create_controls_hierarchy(self.get_color(), radius=self.get_control_radius())

    def change_control_radius_cmd(self):
        import control_tools
        importlib.reload(control_tools)

        control_tools.change_control_radius(radius=self.get_control_radius())

    def parent_constrain_controls_cmd(self):
        import control_tools
        importlib.reload(control_tools)

        control_tools.parent_constrain_controls()

    def parent_scale_constraints_cmd(self):
        import control_tools
        importlib.reload(control_tools)

        control_tools.parent_scale_constraints()

    def auto_constrain_joints_to_selected_controls_cmd(self):
        import control_tools
        importlib.reload(control_tools)

        control_tools.auto_constrain_joints_to_selected_controls()

    def mirror_controls_cmd(self):
        import control_tools
        importlib.reload(control_tools)

        control_tools.mirror_controls()