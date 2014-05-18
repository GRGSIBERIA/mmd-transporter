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
import expgen
import rigidgen

class LoadMMD(maya.OpenMayaMPx.MPxCommand):
  def __init__(self):
    maya.OpenMayaMPx.MPxCommand.__init__(self)


  @classmethod
  def syntaxCreator(cls):
    syntax = maya.OpenMaya.MSyntax()
    syntax.addFlag("-inc", "-incandescense", maya.OpenMaya.MSyntax.kNoArg)
    return syntax


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
    return group


  def _groupExpression(self, blendShapeNames, mother):
    expgroup = maya.cmds.group(n="expresssion", w=True, em=True)
    maya.cmds.parent(expgroup, mother)
    for gname in blendShapeNames:
      maya.cmds.parent(gname, expgroup)
    

  def _createData(self, argData):
    filePath = self._getPath()
    if filePath != None:
      extName = self._getExt(filePath)
      mmdData = self._readData(filePath, extName)
      mpoly.MMDPoly.mmdData = mmdData

      # ポリゴンの生成
      meshName, polyName = meshgen.MeshGenerator.CreatePolyNodes()
      #maya.cmds.polyNormal(polyName, normalMode=0, userNormalMode=0, ch=1)  # 表示が変になるのでノーマルを逆転

      # マテリアルの生成
      incandescenseFlag = argData.isFlagSet("-inc")   # マテリアルの白熱光をMAXにするかどうか
      genMaterial = matgen.MaterialGenerator(mmdData, filePath)
      genMaterial.generate(meshName, incandescenseFlag)

      # Blend Shapeの生成
      #genExp = expgen.ExpressionGenerator(mmdData, filePath)
      #blendShapeNames = genExp.generate(polyName)

      # ボーンの生成
      genBone = bonegen.BoneGenerator(mmdData, filePath)
      jointNames, noparentBonesIndices = genBone.generate(True) #True = humanIkFlug

      # 付与親生成
      genEstab = estabgen.EstablishGenerator(mmdData)
      genEstab.generate(jointNames)

      # スキニング
      skinningFlag = self._skinning(polyName, jointNames, mmdData)

      if skinningFlag:
        # ウェイト
        histories = maya.cmds.listHistory(polyName)
        skinCluster = maya.cmds.ls(histories, type="skinCluster")[0]
        genSkin = skingen.SkinGenerator(mmdData)
        genSkin.generate(skinCluster, jointNames, polyName)

      genRigid = rigidgen.RigidBodyGenerator(mmdData, filePath)
      genRigid.generate(jointNames)

      #グループ化
      mother = self._grouping(polyName, jointNames, noparentBonesIndices)
      #self._groupExpression(blendShapeNames, mother)


  def doIt(self, args):
    try:
      argData = maya.OpenMaya.MArgDatabase(self.syntax(), args)
    except:
      pass
    else:
      self._createData(argData)