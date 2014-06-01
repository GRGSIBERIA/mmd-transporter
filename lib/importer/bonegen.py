#-*- encoding: utf-8

import maya.OpenMaya
import maya.OpenMayaMPx
import maya.cmds

import os.path
import csv
import re

import util
import filemanager as filemng

class BoneGenerator:

  def __init__(self, mmdData, filePath):
    self.mmdData = mmdData
    self.constPI = 180.0 / 3.141592653589793
    directory = os.path.dirname(filePath)
    self.nameDict, self.dictFlag = filemng.openCSV(directory, "bonedict.csv")


  def _createJoints(self, bones):
    noparentBones = []
    jointNames = []
    for i in range(len(bones)):
      boneName = "joint"
      if self.dictFlag:
        boneName = self.nameDict[i]
      pos = bones[i].position

      if bones[i].parent_index == -1:
        noparentBones.append(i)

      maya.cmds.select(d=True)
      jointName = ""
      try:
        jointName = maya.cmds.joint(p=[pos.x, pos.y, -pos.z], name=boneName)
      except:
        jointName = maya.cmds.joint(p=[pos.x, pos.y, -pos.z])   # 稀に不正な名前のボーンが存在する
      
      util.setJpName(jointName, bones[i].name)

      jointNames.append(jointName)
    return jointNames, noparentBones


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


  def _lockHideAttributes(self, jointName, disableType, lockFlag):
    axis = ["x", "y", "z"]
    for elem in axis:
      maya.cmds.setAttr("%s.%s%s" % (jointName, disableType, elem), lock=lockFlag, channelBox=False, keyable=False)


  def _settingDrawStyle(self, bones, jointNames):
    for i in range(len(bones)):
      visible = 0 if bones[i].getVisibleFlag() else 2
      visible = 2 if bones[i].getIkFlag() else visible
      maya.cmds.setAttr("%s.drawStyle" % jointNames[i], visible)


  # 回転・移動・操作フラグからLockとHideを各チャンネルに行う
  def _inspectOperationFlag(self, bones, jointNames, humanIkFlag):
    for i in range(len(bones)):
      lockFlag = not humanIkFlag
      jointName = jointNames[i]

      if not bones[i].getRotatable() or not bones[i].getManipulatable():
        self._lockHideAttributes(jointName, "r", lockFlag)
      if not bones[i].getTranslatable() or not bones[i].getManipulatable():
        self._lockHideAttributes(jointName, "t", lockFlag)

      if bones[i].getFixedAxisFlag():
        maya.cmds.setAttr("%s.rz" % jointName, lock=lockFlag, channelBox=False, keyable=False)
        maya.cmds.setAttr("%s.ry" % jointName, lock=lockFlag, channelBox=False, keyable=False)

      util.setBoolean(jointName, "manipulatable", bones[i].getManipulatable())
      #self._lockHideAttributes(jointName, "s")  # スケールは基本的に使えない
      #maya.cmds.setAttr("%s.v" % jointName, lock=True, channelBox=False, keyable=False)


  # 回転行列（XYZ軸）からオイラー角を求める
  def _rotationMatrixToEulerAngle(self, xAxis, yAxis, zAxis):
    # Z要素は反転させる
    rotateMatrixArray = [
      xAxis[0], xAxis[1], -xAxis[2], 0.0,
      yAxis[0], yAxis[1], -yAxis[2], 0.0,
      zAxis[0], zAxis[1], -zAxis[2], 0.0,
      0.0, 0.0, 0.0, 1.0]
    rotateMatrix = maya.OpenMaya.MMatrix()
    maya.OpenMaya.MScriptUtil.createMatrixFromList(rotateMatrixArray, rotateMatrix)
    transform = maya.OpenMaya.MTransformationMatrix(rotateMatrix)
    order = maya.OpenMaya.MTransformationMatrix.kXYZ
    eulerAngle = transform.eulerRotation().asVector()
    return eulerAngle


  def _crossProduct(self, a, b):
    array = [
      a[1]*b[2]-a[1]*b[1],
      a[2]*b[0]-a[2]*b[2],
      a[0]*b[1]-a[0]*b[0]]
    return array


  def _setJointOrient(self, constPI, jointName, xAxis, yAxis, zAxis):
    eulerAngle = self._rotationMatrixToEulerAngle(xAxis, yAxis, zAxis)
    maya.cmds.setAttr("%s.jointOrientX" % jointName, eulerAngle.x * constPI)
    maya.cmds.setAttr("%s.jointOrientY" % jointName, eulerAngle.y * constPI)
    maya.cmds.setAttr("%s.jointOrientZ" % jointName, eulerAngle.z * constPI)


  # ローカル軸があればJoint Orientを設定する
  def _rectifyJointOrientation(self, bones, jointNames):
    for i in range(len(bones)):
      if bones[i].getLocalCoordinateFlag():
        xAxis = bones[i].local_x_vector
        zAxis = bones[i].local_z_vector
        yAxis = self._crossProduct(zAxis, xAxis)
        self._setJointOrient(self.constPI, jointNames[i], xAxis, yAxis, zAxis)
  

  # 軸制限があれば軸制限する
  def _rectifyAxisLimt(self, bones, jointNames):
    for i in range(len(bones)):
      if bones[i].getFixedAxisFlag() and not bones[i].getLocalCoordinateFlag():
        xAxis = bones[i].fixed_axis
        zAxis = self._crossProduct([0.0, 1.0, 0.0], xAxis)
        yAxis = self._crossProduct(zAxis, xAxis)

        self._setJointOrient(self.constPI, jointNames[i], xAxis, yAxis, zAxis)


  def _rectifyEstablishAxis(self, bones, jointNames):
    for i in range(len(bones)):
      if bones[i].getExternalRotationFlag():
        index = bones[i].effect_index
        x = maya.cmds.getAttr("%s.jointOrientX" % jointNames[index])
        y = maya.cmds.getAttr("%s.jointOrientY" % jointNames[index])
        z = maya.cmds.getAttr("%s.jointOrientZ" % jointNames[index])
        maya.cmds.setAttr("%s.jointOrientX" % jointNames[i], x)
        maya.cmds.setAttr("%s.jointOrientY" % jointNames[i], y)
        maya.cmds.setAttr("%s.jointOrientZ" % jointNames[i], z)


  # この並び方通りにjoint.sideの番号が振られている
  jointSide = [u"中", u"左", u"右"]

  # ボーンの種類，プルダウンの連番と同じ並び
  jointType = [
    [],
    [u"センター", u"全ての親"],
    [u"下半身", u"腰", u"足"],
    [u"ひざ", u"膝"],
    [u"足首"],
    [u"つま先", u"爪先"],
    [u"上半身"],
    [u"首"],
    [u"頭"],
    [u"肩", u"鎖骨"],   # collar?
    [u"腕", u"腕捩"],
    [u"肘", u"ひじ"],
    [u"手首", u"手捩", u"手首捩"], # hand
    [],
    [u"親指"],
    [],
    [],
    [],
    [],
    [u"人指", u"人差し指", u"人差指"],
    [u"中指"],
    [u"薬指"],
    [u"小指"],
    []]   # ここから先もたくさんあるけど無視する
  # キャンセル, ～先は無効


  def _labelingJointSide(self, bone, jointName):
    for js in [2, 1, 0]:    # 中指などが存在するので後ろが優先
      result = bone.name.find(BoneGenerator.jointSide[js])
      if result != -1:
        maya.cmds.setAttr("%s.side" % jointName, js)
        return True


  def _ignoreLabeling(self, bone):
    r = bone.name.find(u"先")
    if r >= len(bone.name) - 1:
      return True

    ignore = [u"キャンセル", u"ｷｬﾝｾﾙ", u"ダミー", u"ﾀﾞﾐｰ", u"補助", u"IK", u"ＩＫ"]
    for target in ignore:
      r = bone.name.find(target)
      if r != -1:
        return True
    return False


  def _labelingJointType(self, bone, jointName):
    if self._ignoreLabeling(bone):
      return True   # 強制脱出

    jtArray = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 19, 20, 21, 22]
    for jt in range(len(jtArray)):
      for jName in BoneGenerator.jointType[jt]:
        result = bone.name.find(jName)
        if result != -1:
          maya.cmds.setAttr("%s.type" % jointName, jt)
          return True


  def _jointLabeling(self, bones, jointNames):
    # 既にベースになる名前はあるのでdictFlagで回避する必要はない
    for i in range(len(bones)):
      self._labelingJointSide(bones[i], jointNames[i])
      self._labelingJointType(bones[i], jointNames[i])


  def generate(self, humanIkFlag):
    bones = self.mmdData.bones
    jointNames, noparentBones = self._createJoints(bones)
    self._settingDrawStyle(bones, jointNames)  # 本番ではコメントを消す
    self._jointLabeling(bones, jointNames)
    self._rectifyJointOrientation(bones, jointNames)
    self._rectifyAxisLimt(bones, jointNames)
    self._rectifyEstablishAxis(bones, jointNames)
    self._connectJoints(bones, jointNames)
    self._inspectOperationFlag(bones, jointNames, humanIkFlag) # これを実行するとHuman IK使えなくなる
    return jointNames, noparentBones