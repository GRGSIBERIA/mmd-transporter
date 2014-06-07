#-*- encoding: utf-8

import maya.cmds

class AxisBase:

  def getEnableFlagList(self, boneNames, flagType):
    enables = []
    for bone in boneNames:
      flag = maya.cmds.getAttr("%s.enable%s" % (bone, flagType))
      enables += True if flag == 1 else False
    return enables


  def getJointOrients(self, boneName):
    x = maya.cmds.getAttr("%s.jointOrientX" % boneName)
    y = maya.cmds.getAttr("%s.jointOrientY" % boneName)
    z = maya.cmds.getAttr("%s.jointOrientZ" % boneName)
    return [x, y, z]


  def __init__(self):
    pass


class FixedAxis(AxisBase):

  def _calcOrientJoint(self, boneName):
    orient = self.getJointOrients(boneName)


  def _getFixedAxis(self):
    fixedAxises = []
    for i in range(len(self.boneNames)):
      boneName = self.boneNames[i]
      if self.enables[i]:
        pass
      else:
        fixedAxises.append(None)
    return fixedAxises
      

  def __init__(self, boneNames):
    AxisBase.__init__(self)
    self.boneNames = boneNames
    self.enables = getEnableFlagList(self.boneNames, "FixedAxis")
    self.fixedAxises = self._getFixedAxis()


class LocalAxis(AxisBase):

  def __init__(self, boneNames):
    AxisBase.__init__(self)
    self.boneNames = boneNames
    self.enables = getEnableFlagList(self.boneNames, "LocalAxis")