#-*- encoding: utf-8

import maya.cmds
import util

class GroupGenerator:

  def __init__(self):
    self.group = maya.cmds.group(n="mmdModelGroup", w=True, em=True)
    util.setBoolean(self.group, "mmdModel", True)


  def groupingStandard(self, polyName, jointNames, noparentBonesIndices):
    maya.cmds.select(d=True)
    boneGroup = maya.cmds.group(n="bones", w=True, em=True)
    util.setString(boneGroup, "nodeType", "boneGroup")
    maya.cmds.parent(boneGroup, self.group)
    maya.cmds.parent(polyName, self.group)
    for i in noparentBonesIndices:
      maya.cmds.parent(jointNames[i], boneGroup)


  def groupingBlendShapes(self, blendShapeNames):
    expgroup = maya.cmds.group(n="blendShapes", w=True, em=True)
    util.setString(expgroup, "nodeType", "blendShapeGroup")
    maya.cmds.parent(expgroup, self.group)
    for gname in blendShapeNames:
      maya.cmds.parent(gname, expgroup)


  def groupingRigidbodies(self, rigidbodies):
    rigidGroup = maya.cmds.group(n="rigidbodies", w=True, em=True)
    maya.cmds.parent(rigidGroup, self.group)
    util.setString(rigidGroup, "nodeType", "rigidbodyGroup")
    for rigidName in rigidbodies:
      maya.cmds.parent(rigidName, rigidGroup)


  def groupingConstraints(self, constraints):
    constGroup = maya.cmds.group(n="constraints", w=True, em=True)
    maya.cmds.parent(constGroup, self.group)
    util.setString(constGroup, "nodeType", "constraintGroup")
    for constName in constraints:
      maya.cmds.parent(constName, constGroup)