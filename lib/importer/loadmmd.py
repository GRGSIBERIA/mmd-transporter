#-*- encoding: utf-8
import sys
import os.path
import maya.OpenMayaMPx
import maya.cmds

import pymeshio.pmx.reader
import pymeshio.pmd.reader

import dictmaker
import mmdpoly as mpoly
import meshgen
import matgen
import bonegen
import skingen
import estabgen
import expgen
import rigidgen
import grpgen
import util

class LoadMMD(maya.OpenMayaMPx.MPxCommand):
  def __init__(self):
    maya.OpenMayaMPx.MPxCommand.__init__(self)


  @classmethod
  def syntaxCreator(cls):
    syntax = maya.OpenMaya.MSyntax()
    syntax.addFlag("-inc", "-incandescense", maya.OpenMaya.MSyntax.kNoArg)
    syntax.addFlag("-rgd", "-rigidbody", maya.OpenMaya.MSyntax.kNoArg)
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


  def _createData(self, argData):
    filePath = self._getPath()
    if filePath != None:
      extName = self._getExt(filePath)
      mmdData = self._readData(filePath, extName)
      mpoly.MMDPoly.mmdData = mmdData
      dmaker = dictmaker.DictMaker(mmdData)

      # ポリゴンの生成
      meshName, polyName = meshgen.MeshGenerator.CreatePolyNodes()
      #maya.cmds.polyNormal(polyName, normalMode=0, userNormalMode=0, ch=1)  # 表示が変になるのでノーマルを逆転

      # マテリアルの生成
      incandescenseFlag = argData.isFlagSet("-inc")   # マテリアルの白熱光をMAXにするかどうか
      genMaterial = matgen.MaterialGenerator(mmdData, filePath, dmaker.materials)
      genMaterial.generate(meshName, incandescenseFlag)

      # Blend Shapeの生成
      genExp = expgen.ExpressionGenerator(mmdData, filePath, dmaker.morphs)
      blendShapeNames = genExp.generate(polyName)

      # ボーンの生成
      genBone = bonegen.BoneGenerator(mmdData, filePath, dmaker.bones)
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

      if argData.isFlagSet("-inc"):
        pass
      genRigid = rigidgen.RigidBodyGenerator(mmdData, filePath, dmaker.rigidbodies)
      rigidNames, constraintNames = genRigid.generate(jointNames)

      #グループ化
      genGroup = grpgen.GroupGenerator()
      genGroup.groupingStandard(polyName, jointNames, noparentBonesIndices)
      genGroup.groupingBlendShapes(blendShapeNames)
      genGroup.groupingRigidbodies(rigidNames)
      genGroup.groupingConstraints(constraintNames)



  def doIt(self, args):
    try:
      argData = maya.OpenMaya.MArgDatabase(self.syntax(), args)
    except:
      pass
    else:
      self._createData(argData)