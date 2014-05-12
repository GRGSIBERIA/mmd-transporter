#-*- encoding: utf-8

import maya.OpenMaya
import maya.OpenMayaMPx
import maya.cmds

import kakasi

class BoneGenerator:
  def __init__(self, mmdData):
    self.mmdData = mmdData

  def _translateJapanese(self, boneName):
    romaji = kakasi.hepburn(boneName)
    return romaji

  def _createJoints(self, bones):
    jointNames = []
    for i in range(len(bones)):
      boneName = self._translateJapanese(bones[i].name)
      pos = bones[i].position
      maya.cmds.select(d=True)
      translatedName = self._translateJapanese(bones[i].name)
      jointName = maya.cmds.joint(p=[pos.x, pos.y, -pos.z], name=boneName)
      jointNames.append(jointName)
    return jointNames

  def _connectJoints(self, bones, jointNames):
    for i in range(len(bones)):
      parentInd = bones[i].parent_index
      if parentInd != -1:   # 親のないボーンは無視
        childBoneName = jointNames[i]
        parentBoneName = jointNames[parentInd]
        try:
          maya.cmds.connectJoint(childBoneName, parentBoneName, pm=True)
        except:
          print ("topology error:", i, childBoneName, parentBoneName)

  def _lockHideAttributes(self, jointName, disableType):
    axis = ["x", "y", "z"]
    for elem in axis:
      maya.cmds.setAttr("%s.%s%s" % (jointName, disableType, elem), lock=True, channelBox=False, keyable=False)

  def _inspectOperationFlag(self, bones, jointNames):
    for i in range(len(bones)):
      visible = 0 if bones[i].getVisibleFlag() else 2
      jointName = jointNames[i]
      maya.cmds.setAttr("%s.drawStyle" % jointName, visible)

      if not bones[i].getRotatable() or not bones[i].getManipulatable():
        self._lockHideAttributes(jointName, "r")
      if not bones[i].getTranslatable() or not bones[i].getManipulatable():
        self._lockHideAttributes(jointName, "t")

      self._lockHideAttributes(jointName, "s")  # スケールは基本的に使えない
      maya.cmds.setAttr("%s.v" % jointName, lock=True, channelBox=False, keyable=False)

  def _rotationMatrixToEulerAngle(self, xAxis, yAxis, zAxis):
    rotateMatrixArray = [
          xAxis[0], xAxis[1], xAxis[2], 0.0,
          yAxis[0], yAxis[1], yAxis[2], 0.0,
          zAxis[0], zAxis[1], zAxis[2], 0.0,
          0.0, 0.0, 0.0, 1.0]
        rotateMatrix = maya.OpenMaya.MMatrix()
        maya.OpenMaya.MScriptUtil.createMatrixFromList(rotateMatrixArray, rotateMatrix)
        transform = maya.OpenMaya.MTransformationMatrix(rotateMatrix)
        order = maya.OpenMaya.MTransformationMatrix.kXYZ
        eulerAngle = transform.eulerRotation().asVector()
        return eulerAngle

  def _rectifyJointOrientation(self, bones, jointNames):
    constPI = 180.0 / 3.141592653589793
    for i in range(len(bones)):
      if bones[i].getLocalCoordinateFlag():
        xAxis = bones[i].local_x_vector
        zAxis = bones[i].local_z_vector
        # Z軸は必ず反転させる
        yAxis = [
          zAxis.y*-xAxis.z-(-zAxis.z)*xAxis.x,
          -zAxis.z*xAxis.x-zAxis.x*-xAxis.z,
          zAxis.x*xAxis.y-zAxis.y*xAxis.x]

        eulerAngle = self._rotationMatrixToEulerAngle(xAxis, yAxis, zAxis)
        
        maya.cmds.setAttr("%s.jointOrientX" % jointNames[i], eulerAngle.x * constPI)
        maya.cmds.setAttr("%s.jointOrientY" % jointNames[i], eulerAngle.y * constPI)
        maya.cmds.setAttr("%s.jointOrientZ" % jointNames[i], eulerAngle.z * constPI)

  def generate(self):
    bones = self.mmdData.bones
    jointNames = self._createJoints(bones)
    self._rectifyJointOrientation(bones, jointNames)
    self._connectJoints(bones, jointNames)
    self._inspectOperationFlag(bones, jointNames)