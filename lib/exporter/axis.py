#-*- encoding: utf-8

import maya.cmds
import maya.OpenMaya

import pymeshio.common

class AxisBase:

  def getEnableFlagList(self, boneNames, flagType):
    enables = []
    for bone in boneNames:
      try:
        flagBuf = maya.cmds.getAttr("%s.enable%s" % (bone, flagType))
        flag = True if flagBuf == 1 else False
        enables.append(flag)
      except:
        print "%s is not attached enable%s." % (bone, flagType)
        enables.append(False)   # 何らかの理由でenablehogehogeが追加されてないが支障なし
    return enables


  def getJointOrients(self, boneName):
    x = maya.cmds.getAttr("%s.jointOrientX" % boneName)
    y = maya.cmds.getAttr("%s.jointOrientY" % boneName)
    z = maya.cmds.getAttr("%s.jointOrientZ" % boneName)
    return [x, y, z]


  def getMatrix(self, boneName):
    orient = self.getJointOrients(boneName)
    rotation = maya.OpenMaya.MEulerRotation(orient[0], orient[1], orient[2])
    return rotation.asMatrix()


  def getAxis(self, matrix, col):
    axis = maya.OpenMaya.MVector(matrix(col, 0), matrix(col, 1), -matrix(col, 2))
    return pymeshio.common.Vector3(axis.x, axis.y, axis.z)


  def __init__(self, boneNames):
    self.boneNames = boneNames


class FixedAxis(AxisBase):

  def _calcAxis(self, boneName):
    matrix = self.getMatrix(boneName)
    vector = self.getAxis(matrix, 0)
    return vector


  def _getFixedAxis(self):
    fixedAxises = []
    for i in range(len(self.boneNames)):
      boneName = self.boneNames[i]
      if self.enables[i]:
        axis = self._calcAxis(boneName)
        fixedAxises.append(axis)
      else:
        fixedAxises.append(None)
    return fixedAxises
      

  def __init__(self, boneNames):
    AxisBase.__init__(self, boneNames)
    self.enables = self.getEnableFlagList(self.boneNames, "FixedAxis")
    self.axises = self._getFixedAxis()


class LocalAxis(AxisBase):

  def _calcLocal(self, boneName):
    matrix = self.getMatrix(boneName)
    vectorX = self.getAxis(matrix, 0)
    vectorZ = self.getAxis(matrix, 2)
    return [vectorX, vectorZ]
    

  def _getLocalAxis(self):
    localAxises = []
    for i in range(len(self.boneNames)):
      boneName = self.boneNames[i]
      if self.enables[i]:
        axis = self._calcLocal(boneName)
        localAxises.append(axis)
      else:
        localAxises.append(None)
    return localAxises


  def __init__(self, boneNames):
    AxisBase.__init__(self, boneNames)
    self.enables = self.getEnableFlagList(self.boneNames, "LocalAxis")
    self.axises = self._getLocalAxis()
