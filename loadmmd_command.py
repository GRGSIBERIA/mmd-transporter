#-*- encoding: utf-8
class LoadMMDCommand(maya.OpenMayaMPx.MPxCommand):
  def __init__(self):
    maya.OpenMayaMPx.MPxCommand.__init__(self)

  @classmethod
  def cmdCreator(cls):
    return maya.OpenMayaMPx.asMPxPtr(cls())

  def doIt(self, args):
    poly = maya.cmds.createNode('transform')
    mesh = maya.cmds.createNode('mesh', parent=poly)
    maya.cmds.sets(mesh, add='initialShadingGroup')
    spoly = maya.cmds.createNode('transportedMMD1')
    maya.cmds.connectAttr(spoly + '.outputMesh', mesh + '.inMesh') 
