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
      bone = pymeshio.pmx.Bone(None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
      bones.append(bone)
    return bones


  def _setBoneNames(self):
    for i in range(len(self.bones)):
      bone = self.bones[i]
      bone.name = maya.cmds.getAttr("%s.jpName" % self.boneNames[i])
      bone.english_name = self.boneNames[i]


  def _setBonePositions(self):
    for i in range(len(self.bones)):
      bone = self.bones[i]
      pos = maya.cmds.xform(self.boneNames[i], q=True, t=True, a=True)
      bonePos = pymeshio.common.Vector3(pos[0], pos[1], -pos[2])  # Z軸反転
      bone.position = bonePos


  def _setBoneAttr(self):
    self._setBoneNames()
    self._setBonePositions()


  def __init__(self, boneNames, establish, localAxis, fixedAxis):
    self.boneNames = boneNames
    self.boneNameToIndex = self._getBoneNamesToIndex()
    self.bones = self._createBones()
    self._setBoneAttr()