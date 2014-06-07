#-*- encoding: utf-8

import maya.cmds
import maya.OpenMaya

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

  def _calcAxis(self, boneName):
    orient = self.getJointOrients(boneName)
    rotation = maya.OpenMaya.MEulerRotation(orient[0], orient[1], orient[2])
    quaternion = rotation.asQuaternion()
    vector = maya.OpenMaya.MVector(0, 0, 0)
    double = maya.OpenMaya.MScriptUtil()
    double.createFromDouble(0.0)
    pointer = double.asDoublePtr()
    vector, angle = quaternion.getAxisAngle(vector, pointer) # 引数がMVector&, double&なので渡し方がわからん
    return vector


  def _getFixedAxis(self):
    fixedAxises = []
    for i in range(len(self.boneNames)):
      boneName = self.boneNames[i]
      if self.enables[i]:
        axis = self._calcAxis(boneNames[i])
        fixedAxises.append(vector)
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

#import maya.cmds
#import maya.OpenMaya
#
#rot = maya.OpenMaya.MEulerRotation(0, 0, 0)
#qua = rot.asQuaternion()
#vec = maya.OpenMaya.MVector(0, 0, 0)
#dou = maya.OpenMaya.MScriptUtil()
#dou.createFromDouble(0.0)
#ptr = dou.asDoublePtr()
#res = qua.getAxisAngle(vec, ptr)
#print vec
