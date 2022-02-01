import maya.cmds as cmds
import importlib


class tools_ui:
    def __init__(self):
        self.m_window = 'toolsUIWin'
        self.override_color = 0
        self.colorSlider = ''
        self.controlRadiusField = ''
        self.renameField = ''

    def create(self):
        self.delete()

        self.m_window = cmds.window(self.m_window, title="Tools", resizeToFitChildren=True)
        column = cmds.columnLayout(parent=self.m_window)

        # sequential renamer
        self.renameField = cmds.textFieldButtonGrp(parent=column,
                                label="Sequential Renamer",
                                text="arm_##_jnt",
                                buttonLabel="Rename",
                                buttonCommand=lambda *x: self.sequential_rename_cmd())

        # change color
        self.colorSlider = cmds.colorIndexSliderGrp(parent=column,
                                                    label="OverrideColor",
                                                    minValue=1,
                                                    maxValue=32)
        cmds.button(parent=column, label="Apply Color", command=lambda *x: self.override_color_apply_cmd())
        cmds.button(parent=column, label="Apply Color To Hierarchy", command=lambda *x: self.override_color_apply_hierarchy_cmd())

        # controls
        self.controlRadiusField = cmds.floatFieldGrp(parent=column, label="Control Radius", value1=1)
        cmds.button(parent=column, label="Create Controls", command=lambda *x: self.create_controls_cmd())
        cmds.button(parent=column, label="Create Controls From Hierarchy", command=lambda *x: self.create_controls_hierarchy_cmd())

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
        import tools
        importlib.reload(tools)

        tools.create_controls(self.get_color(), radius=self.get_control_radius())


    def create_controls_hierarchy_cmd(self):
        import tools
        importlib.reload(tools)

        tools.create_controls_hierarchy(self.get_color(), radius=self.get_control_radius())

    def sequential_rename_cmd(self):
        import tools
        importlib.reload(tools)

        name_pattern = cmds.textFieldButtonGrp(self.renameField, q=True, text=True)
        tools.sequential_rename_selection(name_pattern)


# Demonstration
my_ui = tools_ui()
my_ui.create()