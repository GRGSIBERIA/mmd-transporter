#-*- encoding: utf-8
import sys
import os.path
import maya.OpenMayaMPx
import maya.cmds

import pymeshio.pmx.reader
import pymeshio.pmd.reader

import dictionary
import mmdpoly
import importer.meshgen as meshgen
import importer.matgen as matgen
import importer.bonegen as bonegen
import importer.skingen as skingen
import importer.estabgen as estabgen
import importer.expgen as expgen
import importer.rigidgen2 as rigidgen
import importer.grpgen as grpgen
import util

class LoadMMD(maya.OpenMayaMPx.MPxCommand):
  def __init__(self):
    maya.OpenMayaMPx.MPxCommand.__init__(self)


  @classmethod
  def syntaxCreator(cls):
    syntax = maya.OpenMaya.MSyntax()
    #syntax.addFlag("-inc", "-incandescense", maya.OpenMaya.MSyntax.kNoArg)
    syntax.addFlag("-r", "-rigidbody", maya.OpenMaya.MSyntax.kNoArg) # kNoArgは2つまでしか登録できない？
    #syntax.addFlag("-nr", "-norigidbody", maya.OpenMaya.MSyntax.kNoArg)
    return syntax


  def _getPath(self):
    filterName = "PMD/PMX (*.pmd *pmx);;PMD (*.pmd);;PMX (*.pmx)"
    fpath = maya.cmds.fileDialog2(ds=2, cap="Selet PMD/PMX", ff=filterName, fm=1)
    if fpath != None:
      return fpath[0]
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

    print filePath

    if filePath != None:
      extName = self._getExt(filePath)
      mmdData = self._readData(filePath, extName)

      mmdpoly.MMDPoly.mmdData = mmdData

      dict = dictionary.Dictionary(mmdData)

      # ポリゴンの生成
      meshName, polyName = meshgen.MeshGenerator.CreatePolyNodes()
      #maya.cmds.polyNormal(polyName, normalMode=0, userNormalMode=0, ch=1)  # 表示が変になるのでノーマルを逆転

      # マテリアルの生成
      #incandescenseFlag = argData.isFlagSet("-inc")   # マテリアルの白熱光をMAXにするかどうか
      genMaterial = matgen.MaterialGenerator(mmdData, filePath, dict.materials)
      #genMaterial.generate(meshName, incandescenseFlag)
      genMaterial.generate(meshName, False)

      # Blend Shapeの生成
      genExp = expgen.ExpressionGenerator(mmdData, filePath, dict.morphs)
      blendShapeNames = genExp.generate(polyName)

      # ボーンの生成
      genBone = bonegen.BoneGenerator(mmdData, filePath, dict.bones)
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

      rigidbodyFlag = argData.isFlagSet("-r")
      #rigidbodyFlag = False     # 
      
      if rigidbodyFlag:
        genRigid = rigidgen.RigidBodyGenerator(mmdData, filePath, dict.rigidbodies)
        rigidNames, constraintNames = genRigid.generate(jointNames)

        #グループ化
        genGroup = grpgen.GroupGenerator()
        genGroup.groupingStandard(polyName, jointNames, noparentBonesIndices)
        genGroup.groupingBlendShapes(blendShapeNames)
        genGroup.groupingRigidbodies(rigidNames)
        genGroup.groupingConstraints(constraintNames)



  def doIt(self, args):
    try:
      self.argData = maya.OpenMaya.MArgDatabase(self.syntax(), args)    # このコードを実行するとなぜか落ちる
    except:
      pass
    else:
      self._createData(self.argData)
      pass