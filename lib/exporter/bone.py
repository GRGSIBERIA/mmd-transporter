#-*- encoding: utf-8

import maya.cmds
import pymeshio.pmx
import pymeshio.common

class Bone:

  # ボーンの並び順が原因でイカれる可能性あり
  def _getBoneNamesToIndex(self):
    boneNameToIndex = {}
    for i in range(len(self.boneNames)):
      boneNamesToIndex[self.boneNames[i]] = i
    return boneNameToIndex


  def _createBones(self):
    bones = []
    for i in range(len(self.boneNames)):
      bone = pymeshio.pmx.Bone(None, None, None, None, None, None)
      bones.append(bone)
    return bones


  def _setBoneName(self, bone, boneName):
    return maya.cmds.getAttr("%s.jpName" % self.boneName)


  def _setParentIndex(self, boneName):
    parent = maya.cmds.listRelatives(p=True)
    if parent != None:
      return self.boneNameToIndex(parent[0])
    return -1


  def _setBonePosition(self, bone, boneName):
    pos = maya.cmds.xform(self.boneName, q=True, t=True, a=True)
    bonePos = pymeshio.common.Vector3(pos[0], pos[1], -pos[2])  # Z軸反転
    return bonePos


  def _setBoneLimitation(self, bone, i):
    if self.localAxis.enables[i]:
      self.bone.flag += pymeshio.pmx.BONEFLAG_HAS_LOCAL_COORDINATE
      self.bone.local_x_vector = self.localAxis.axises[i][0]
      self.bone.local_z_vector = self.localAxis.axises[i][1]
    if self.fixedAxis.enables[i]:
      self.bone.flag += pymeshio.pmx.BONEFLAG_HAS_FIXED_AXIS
      self.bone.fixed_axis = self.fixedAxis.axises[i]


  def _setEstablishment(self, bone, boneName):
    establishFlag = maya.cmds.getAttr("%s.enableEstablish" % boneName)
    if establishFlag:
      if establish.rotate.has_key(boneName):
        bone.flag += pymeshio.pmx.BONEFLAG_IS_EXTERNAL_ROTATION
      if establish.translate.has_key(boneName):
        bone.flag += pymeshio.pmx.BONEFLAG_IS_EXTERNAL_TRANSLATION
      parentName = maya.cmds.getAttr("%s.establishParent" % boneName)
      effectFactor = maya.cmds.getAttr("%s.establishFactor" % boneName)
      bone.effect_index = self.boneNameToIndex[parentName]  # 親ボーン名からインデックスへ
      bone.effect_factor = effectFactor


  def _setFlags(self, bone, boneName):
    drawable = maya.cmds.getAttr("%s.drawable" % boneName)
    manipulatable = maya.cmds.getAttr("%s.manipulatable" % boneName)
    rotatable = maya.cmds.getAttr("%s.rotatable" % boneName)
    translatable = maya.cmds.getAttr("%s.translatable" % boneName)
    bone.flag += pymeshio.pmx.BONEFLAG_IS_VISIBLE if drawable else 0
    bone.flag += pymeshio.pmx.BONEFLAG_CAN_MANIPULATE if manipulatable else 0
    bone.flag += pymeshio.pmx.BONEFLAG_CAN_ROTATE if rotatable else 0
    bone.flag += pymeshio.pmx.BONEFLAG_CAN_TRANSLATE if translatable else 0


  def _setBoneAttr(self):
    for i in range(len(self.bones)):
      bone = self.bones[i]
      boneName = self.boneNames[i]
      bone.flag = 0
      bone.english_name = boneName
      bone.name = self._setBoneName(bone, boneName)
      bone.parent_index = self._setParentIndex(boneName)
      bone.position = self._setBonePosition(boneName)
      self._setBoneLimitation(bone, i)
      self._setEstablishment(bone, i)
      self._setFlags(bone, boneName)


  def __init__(self, boneNames, establish, localAxis, fixedAxis):
    self.boneNames = boneNames
    self.boneNameToIndex = self._getBoneNamesToIndex()
    self.establish = establish
    self.localAxis = self.localAxis
    self.fixedAxis = fixedAxis
    self.bones = self._createBones()

    self._setBoneAttr()