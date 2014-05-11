#-*- encoding: utf-8
import sys
import maya.OpenMayaMPx
import maya.cmds

class LoadMMD(maya.OpenMayaMPx.MPxCommand):
  def __init__(self):
    maya.OpenMayaMPx.MPxCommand.__init__(self)

  def doIt(self, args):
    poly = maya.cmds.createNode('transform')
    mesh = maya.cmds.createNode('mesh', parent=poly)
    maya.cmds.sets(mesh, add='initialShadingGroup')
    spoly = maya.cmds.createNode('mmdPoly')
    maya.cmds.connectAttr(spoly + '.outputMesh', mesh + '.inMesh') 