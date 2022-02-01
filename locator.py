import maya.cmds as cmds

def locator():
    sels = cmds.ls(sl=True)
    
    bbox = cmds.xform(sels, q=True, boundingBox=True, ws=True)
    
    mid = [0,0,0]
    
    for i in range(3):
        mid[i] = (bbox[i] + bbox[i+3]) / 2
    
    loc = cmds.spaceLocator(position=[0,0,0], absolute=True)[0] 
    
    cmds.xform(loc,translation=mid, ws=True)


def joints_from_sels():
    sels = cmds.ls(sl=True)
    
    for sel in sels:
        pos = cmds.xform(sel, q=True, rotatePivot=True, ws=True)
        
        cmds.select(cl=True)
        jnt = cmds.joint(position=[0,0,0], absolute=True)
        cmds.xform(jnt, translation=pos, ws=True)
        

def parent_from_sels():
    sels = cmds.ls(sl=True)
    
    for i, sel in enumerate(sels):
        print ("%i: $s" % (i, sel))
        if i < (len(sels) - 1):
            cmds.parent(sels[i], sels[i+1])
        
parent_from_sels()
    
    