#-*- encoding: utf-8
import sys
import os.path
import maya.OpenMayaMPx
import maya.cmds

import pymeshio.pmx.reader
import pymeshio.pmd.reader

import mmdpoly as mpoly
import meshgen
import matgen
import bonegen
import skingen
import estabgen

class LoadMMD(maya.OpenMayaMPx.MPxCommand):
  def __init__(self):
    maya.OpenMayaMPx.MPxCommand.__init__(self)

  def _getPath(self):
    filterName = "PMD/PMX (*.pmd *pmx);;PMD (*.pmd);;PMX (*.pmx)"
    path = maya.cmds.fileDialog2(ds=2, cap="Selet PMD/PMX", ff=filterName, fm=1)
    if path != None:
      return path[0]
    return None

  def _getExt(self, filePath):
    root, extType = os.path.splitext(filePath)
    return extType.lower()

  def _readData(self, filePath, extName):
    mmdData = None
    if extName == ".pmd":
      mmdData = pymeshio.pmd.reader.read_from_file(filePath)

    elif extName == ".pmx":
      mmdData = pymeshio.pmx.reader.read_from_file(filePath)
    return mmdData

  def _skinning(self, polyName, jointNames, mmdData):
    maya.cmds.select(polyName)
    for i in range(len(jointNames)):
      name = mmdData.bones[i].name
      if name == u"センター" or name == u"全ての親":
        print "got center"
        maya.cmds.select(jointNames[i], tgl=True)
        maya.cmds.SmoothBindSkin()
        return True
    return False

  def _grouping(self, polyName, jointNames, noparentBonesIndices):
    maya.cmds.select(d=True)
    boneGroup = maya.cmds.group(n="bones", w=True, em=True)
    group = maya.cmds.group(n="mmdModelGroup", w=True, em=True)
    maya.cmds.parent(boneGroup, group)
    maya.cmds.parent(polyName, group)
    for i in noparentBonesIndices:
      maya.cmds.parent(jointNames[i], boneGroup)

  def doIt(self, args):
    filePath = self._getPath()
    if filePath != None:
      extName = self._getExt(filePath)
      mmdData = self._readData(filePath, extName)
      mpoly.MMDPoly.mmdData = mmdData

      # ポリゴンの生成
      meshName, polyName = meshgen.MeshGenerator.CreatePolyNodes()
      maya.cmds.polyNormal(polyName, normalMode=0, userNormalMode=0, ch=1)  # 表示が変になるのでノーマルを逆転

      # マテリアルの生成
      genMaterial = matgen.MaterialGenerator(mmdData, filePath)
      genMaterial.generate(meshName)

      # ボーンの生成
      genBone = bonegen.BoneGenerator(mmdData, filePath)
      jointNames, noparentBonesIndices = genBone.generate(True) #True = humanIkFlug

      # 付与親生成

      # スキニング
      skinningFlag = self._skinning(polyName, jointNames, mmdData)

      if skinningFlag:
        # ウェイト
        histories = maya.cmds.listHistory(polyName)
        skinCluster = maya.cmds.ls(histories, type="skinCluster")[0]
        genSkin = skingen.SkinGenerator(mmdData)
        genSkin.generate(skinCluster, jointNames, polyName)

      #グループ化
      self._grouping(polyName, jointNames, noparentBonesIndices)